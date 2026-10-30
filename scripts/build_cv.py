"""Build the public English academic CV from the site's canonical activity records.

Requires reportlab. Run: python3 scripts/build_cv.py
A CV_FONT_DIR may point to Liberation Sans TTF files for portable font embedding.
"""
from pathlib import Path
import json
import os
import re
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak

ROOT = Path(__file__).resolve().parent.parent
CV = json.loads((ROOT / 'data/cv.json').read_text())
SITE = json.loads((ROOT / 'data/content.json').read_text())['en']
OUT = ROOT / 'Takaya_Nakashima_CV.pdf'
font_candidates = [
    Path(os.environ.get('CV_FONT_DIR', '/nonexistent')),
    Path('/usr/share/fonts/truetype/liberation2'),
    Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pdfjs-dist/standard_fonts',
]
font_dir = next((p for p in font_candidates if (p/'LiberationSans-Regular.ttf').exists()), None)
if font_dir:
    for suffix, file in [('', 'Regular'), ('-Bold', 'Bold'), ('-Italic', 'Italic'), ('-BoldItalic', 'BoldItalic')]:
        pdfmetrics.registerFont(TTFont('CVSans'+suffix, str(font_dir/f'LiberationSans-{file}.ttf')))
    pdfmetrics.registerFontFamily('CVSans', normal='CVSans', bold='CVSans-Bold', italic='CVSans-Italic', boldItalic='CVSans-BoldItalic')
    FONT = 'CVSans'
else:
    FONT = 'Helvetica'
BOLD = FONT+'-Bold'
WINE = colors.HexColor('#641f37')
INK = colors.HexColor('#282329')
MUTED = colors.HexColor('#5c565c')
STYLES = {
    'body': ParagraphStyle('body', fontName=FONT, fontSize=10.7, leading=14.6, textColor=INK, spaceAfter=8),
    'small': ParagraphStyle('small', fontName=FONT, fontSize=9.7, leading=13, textColor=MUTED, spaceAfter=8),
    'section': ParagraphStyle('section', fontName=BOLD, fontSize=12.8, leading=17, textColor=WINE, spaceBefore=16, spaceAfter=9, keepWithNext=True),
    'name': ParagraphStyle('name', fontName=BOLD, fontSize=27, leading=32, textColor=WINE, spaceAfter=7),
    'subtitle': ParagraphStyle('subtitle', fontName=FONT, fontSize=12, leading=16, textColor=INK, spaceAfter=10),
}

def clean(s):
    return str(s).replace('\u2013', '-').replace('\u2014', '-').replace('\u2011', '-').replace('\u2019', "'")

def esc(s):
    return escape(clean(s))

def para(s, style='body'):
    return Paragraph(s, STYLES[style])

def url(href, label):
    return f'<link href="{escape(href, {chr(34): "&quot;"})}" color="#641f37">{esc(label)}</link>'

def section(title):
    story.append(para(esc(title), 'section'))

def entry(date, title, body, href=None):
    title_html = url(href, title) if href else esc(title)
    story.append(KeepTogether([para(f'<b>{esc(date)} | {title_html}</b><br/>{esc(body)}')]))

def author_names(p):
    raw = p['authorsPre'] + p['me'] + p['authorsPost']
    names = []
    for n in raw.split(', '):
        m = re.fullmatch(r'((?:[A-Z]\. ?)+) (.+)', n)
        names.append(m.group(2)+' '+re.sub('[. ]','',m.group(1)) if m else n)
    return ', '.join(names)

def publication(p, index):
    m = CV['publication_metadata'].get(p['href'])
    if m is None:
        m = next((v for v in CV['publication_metadata'].values() if v.get('doi') and p['href'].rstrip('/') == 'https://doi.org/'+v['doi']), None)
    if m is None:
        raise ValueError(f"Missing CV bibliography metadata for {p['title']}")
    authors = m.get('authors', author_names(p)) + m.get('author_suffix', '')
    authors = esc(authors.rstrip('.')).replace('Nakashima T', '<b>Nakashima T</b>')
    title = m.get('title', p['title'])
    venue = m.get('venue', p['venue'])
    details = m.get('details', '')
    target = 'https://doi.org/'+m['doi'] if m.get('doi') else p['href']
    role = 'First and corresponding author' if m.get('corresponding') else 'First author' if p.get('first') else 'Co-first author' if p.get('coFirst') else ''
    citation = f'{index}. {authors}. {esc(title.rstrip('.'))}. <i>{esc(venue)}</i>. {esc(details.rstrip('.'))}.'
    citation += '<br/>'+url(target, 'doi: '+m['doi'] if m.get('doi') else 'Publication record')
    if m.get('code_url'):
        citation += ' | '+url(m['code_url'], 'Analysis code')
    if role:
        citation += f' <font color="#5c565c">| {esc(role)}</font>'
    return KeepTogether([para(citation)])

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8.7)
    canvas.setFillColor(MUTED)
    canvas.drawString(47, A4[1]-31, 'TAKAYA NAKASHIMA, M.D.  |  CURRICULUM VITAE')
    canvas.drawRightString(A4[0]-47, A4[1]-31, 'Updated '+CV['updated'])
    canvas.setStrokeColor(colors.HexColor('#d8cdcf'))
    canvas.line(47, A4[1]-38, A4[0]-47, A4[1]-38)
    canvas.line(47, 37, A4[0]-47, 37)
    canvas.setFont(FONT, 8.5)
    canvas.drawString(47, 24, 'takaya.nakashima@nagasaki-u.ac.jp  |  nakashimatakaya.github.io')
    canvas.drawRightString(A4[0]-47, 24, str(doc.page))
    canvas.restoreState()

story = [para('Takaya Nakashima, M.D.', 'name'), para('Anesthesiologist and biostatistician', 'subtitle')]
story.append(para('Nagasaki University Hospital, Nagasaki, Japan<br/>'+url('mailto:takaya.nakashima@nagasaki-u.ac.jp','takaya.nakashima@nagasaki-u.ac.jp')+'<br/>'+url('https://nakashimatakaya.github.io/en/','Personal website')+' | '+url('https://researchmap.jp/nakataka8228?lang=en','researchmap')+' | '+url('https://orcid.org/0009-0001-4214-3945','ORCID 0009-0001-4214-3945')+' | '+url('https://www.linkedin.com/in/%E8%AA%89%E4%B9%9F-%E4%B8%AD%E5%B3%B6-a26263443/','LinkedIn'), 'small'))
section('Research profile')
story.append(para(esc(CV['research_profile'])))
section('Appointments')
for row in CV['positions']:
    entry(*row)
section('Education')
for row in CV['education']:
    entry(*row)
section('Methods and software')
story.append(para(esc(CV['methods'])))
story.append(para(esc(CV['credential']), 'small'))
section('Professional memberships')
story.append(para('<br/>'.join(esc(date)+' | '+esc(x['name']) for date,x in zip(CV['membership_dates'],SITE['societies'])), 'small'))

story.append(PageBreak())
section('Journal publications')
story.append(para('Author order follows the publication record. First and co-first authorship are marked where applicable. Corresponding authorship is marked for the two 2026 critical care papers.', 'small'))
papers = [p for g in SITE['pubYears'] for p in g['items'] if 'JGLOBAL_ID=202502273103904762' not in p['href']]
for idx, p in enumerate(papers, 1):
    if idx == 8:
        story.append(PageBreak())
        section('Journal publications (continued)')
    story.append(publication(p,idx))
section('Conference abstract')
a = CV['conference_abstract']
story.append(para(esc(a['authors']).replace('Nakashima T', '<b>Nakashima T</b>')+'. '+esc(a['title'])+'. '+esc(a['venue'])+' '+url(a['href'], 'Abstract record')))
section('Research tools')
for x in CV['research_outputs']:
    story.append(KeepTogether([para('<b>'+esc(x['title'])+'</b><br/>'+esc(x['body'])+' '+url(x['href'],x['label']))]))

story.append(PageBreak())
section('Books, chapters, translations and articles')
story.append(para('Japanese-language outputs; English titles below are translations for this CV.', 'small'))
for x in SITE['writings']:
    entry(x['date'],x['title'],x['meta'],x.get('href'))
section('Teaching')
for x in SITE['teaching']:
    date = '2026 - present' if x['date']=='2026–' else 'On-demand course'
    body = x['meta'] + (' '+x['description'] if x.get('description') else '')
    entry(date,x['title'],body,x.get('href'))
section('Awards')
for x in SITE['awards']:
    entry(x['date'],x['title'],x['org'])

story.append(PageBreak())
section('Invited lectures and conference presentations')
story.append(para('Titles translated from Japanese. The SAS entry records the published program listing.', 'small'))
for x in SITE['talks']:
    entry(x['date'], x['title'], CV['talk_metadata'].get(x['date'],x['meta']),x.get('href'))


doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=47, leftMargin=47, topMargin=54, bottomMargin=49, title='Takaya Nakashima, M.D. | Curriculum Vitae', author='Takaya Nakashima', subject='Academic curriculum vitae, updated '+CV['updated'])
doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)
print(OUT)
