from pathlib import Path
import json, html, re
from datetime import date
ROOT=Path(__file__).resolve().parent.parent
D=json.loads((ROOT/'data/content.json').read_text(encoding='utf-8'))
C=json.loads((ROOT/'data/copy.json').read_text(encoding='utf-8'))
R=json.loads((ROOT/'data/research.json').read_text(encoding='utf-8'))
CV=json.loads((ROOT/'data/cv.json').read_text(encoding='utf-8'))
SCHOLAR=CV['google_scholar_url']
UPDATED=date.fromisoformat(CV['updated_iso'])
LINKEDIN='https://www.linkedin.com/in/%E8%AA%89%E4%B9%9F-%E4%B8%AD%E5%B3%B6-a26263443/'
esc=lambda s:html.escape(str(s),quote=True)
def text_lang(text):
 return 'ja' if re.search(r'[\u3040-\u30ff\u3400-\u9fff]', text) else 'en'
def link(url,label,cls='text-link'):
 return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label}<span aria-hidden="true">↗</span></a>'
def section_head(n,label,title,intro=''):
 return f'<div class="section-head" data-reveal><div class="section-rail"><span class="section-number">{n}</span><span class="eyebrow">{label}</span></div><div class="section-heading"><h2>{title}</h2>{f"<p class=section-intro>{esc(intro)}</p>" if intro else ""}</div></div>'
def record(x,lang,kind='talk'):
 meta=esc(x['meta']).replace(' ／ ',' · ').replace('／ ',' · ')
 label='詳細を見る' if lang=='ja' else 'View details'
 tag=esc(x['tag']);title=esc(x['title']);date=esc(x['date'])
 if x.get('href'): title=f'<a href="{esc(x["href"])}" target="_blank" rel="noopener noreferrer">{title}<span class="record-arrow" aria-hidden="true">↗</span></a>'
 desc=f'<p>{esc(x["description"])}</p>' if x.get('description') else ''
 if kind == 'talk':
  when = x['date'].replace('.', '-')
  return (
   f'<li class="talk-entry"><div class="talk-byline"><time datetime="{esc(when)}">{date}</time><span>{tag}</span></div>'
   f'<h4 lang="{text_lang(x["title"])}">{title}</h4><p class="talk-event">{meta}</p>{desc}</li>'
  )
 return f'<li class="record {"upcoming" if x.get("upcoming") else ""}"><div class="record-date"><span>{date}</span><small>{tag}</small></div><div class="record-body"><h3 lang="{text_lang(x["title"])}">{title}</h3><p class="record-meta">{meta}</p>{desc}</div></li>'
def talk_archive(talks, lang):
 groups = {}
 for item in sorted(talks, key=lambda talk: talk['date'], reverse=True):
  year = item['date'].split('.', 1)[0]
  groups.setdefault(year, []).append(item)
 year_links = []
 sections = []
 for index, (year, entries) in enumerate(groups.items()):
  anchor = f'talks-{esc(year)}'
  year_links.append(f'<a href="#{anchor}">{esc(year)}</a>')
  count = len(entries)
  count_label = f'{count}件' if lang == 'ja' else f'{count} talk' + ('s' if count != 1 else '')
  entries_html = ''.join(record(item, lang) for item in entries)
  sections.append(
   f'<details class="talk-year" id="{anchor}"{" open" if index == 0 else ""}><summary><h3>'
   f'<span>{esc(year)}</span><small>{count_label}</small><span class="plus" aria-hidden="true"></span>'
   f'</h3></summary><ol class="talk-entries">{entries_html}</ol></details>'
  )
 nav_label = '講演・学会発表の開催年' if lang == 'ja' else 'Talks by year'
 total = f'全{len(talks)}件' if lang == 'ja' else f'{len(talks)} talks and presentations'
 return (
  f'<div class="talk-index"><span>{total}</span><nav aria-label="{nav_label}">'
  f'{"".join(year_links)}</nav></div>{"".join(sections)}'
 )
def paper(p,year,lang):
 role=('共同筆頭著者' if lang=='ja' else 'Co-first author') if p.get('coFirst') else ('筆頭著者' if lang=='ja' else 'First author') if p.get('first') else ''
 if p.get('corresponding'):
  role=('筆頭・責任著者' if lang=='ja' else 'First and corresponding author') if p.get('first') else ('責任著者' if lang=='ja' else 'Corresponding author')
 if p.get('type')=='conference_abstract':
  role='学会抄録' if lang=='ja' else 'Conference abstract'
 authors=esc(p['authorsPre'])+f'<strong>{esc(p["me"])}</strong>'+esc(p['authorsPost'])
 review=('査読あり' if lang=='ja' else 'Peer reviewed') if p.get('peerReviewed') else ('演題査読あり' if lang=='ja' else 'Reviewed abstract') if p.get('abstractReviewed') else ''
 kind={'letter': ('リサーチレター','Research Letter'), 'correspondence': ('レター（Correspondence）','Correspondence'), 'correction': ('訂正','Correction'), 'preprint': ('プレプリント（査読前）','Preprint; not peer reviewed')}.get(p.get('type'), ('',''))[lang=='en']
 tags=' · '.join(x for x in [review,role,kind] if x)
 note=f'<p class="publication-note">{esc(p["publicationNote"])}</p>' if p.get('publicationNote') else ''
 return f'<li class="paper"><div class="paper-meta"><span>{esc(p["venue"])}</span>{f"<span>{esc(tags)}</span>" if tags else ""}</div><h5 lang="{text_lang(p["title"])}"><a href="{esc(p["href"])}" target="_blank" rel="noopener noreferrer">{esc(p["title"])}<span class="record-arrow" aria-hidden="true">↗</span></a></h5><p class="authors" lang="{text_lang(p["authorsPre"]+p["me"]+p["authorsPost"])}">{authors}</p>{note}</li>'
def publication_groups(rows,lang):
 groups={}
 for year,item in rows: groups.setdefault(year,[]).append(item)
 return ''.join(f'<div class="publication-group"><h4 class="publication-year">{esc(year)}</h4><ol class="paper-list">'+''.join(paper(p,year,lang) for p in items)+'</ol></div>' for year,items in groups.items())
def selected_study(x,lang):
 label='原著論文' if lang=='ja' else 'Read the paper'
 code_link=link(x['code'],'解析コード' if lang=='ja' else 'Analysis code') if x.get('code') else ''
 return f'<article class="selected-study"><div class="study-citation"><p>{esc(x["journal"])}</p><span>{esc(x["year"])} · {esc(x["role"])}</span></div><div class="study-summary"><h4>{esc(x["title"])}</h4><p>{esc(x["body"])}</p><p class="study-methods">{esc(x["methods"])}</p><div class="study-links">{link(x["href"],label)}{code_link}</div></div></article>'
for lang in ['ja','en']:
 en=lang=='en';d=D[lang];cp=C[lang];base='../' if en else './'
 writings=d['writings']
 all_papers=[(g['year'],p) for g in d['pubYears'] for p in g['items']]
 papers=[(y,p) for y,p in all_papers if p.get('type') in {'journal_article','correspondence','letter'}]
 abstracts=[(y,p) for y,p in all_papers if p.get('type')=='conference_abstract']
 nav=[('profile','Profile' if en else 'プロフィール'),('research','Research' if en else '研究・論文'),('writing','Writing' if en else '執筆・発信'),('talks','Talks' if en else '講演'),('teaching','Teaching' if en else '教育')]
 title='Takaya Nakashima, M.D. | Anesthesiology, critical care and biostatistics' if en else '中島誉也 | 臨床と統計の橋渡しを。'
 hero='<span class="hero-line">Clinical care.</span><span class="hero-line"><em>Statistical thinking.</em></span>' if en else '<span class="hero-line">臨床と統計の</span><span class="hero-line"><em>橋渡し</em>を。</span>'
 hreflang='/en/' if en else '/'
 switch='<a href="../" lang="ja" hreflang="ja">日本語</a><span aria-current="page">EN</span>' if en else '<span aria-current="page">JA</span><a href="./en/" lang="en" hreflang="en">EN</a>'
 news=d['news']
 author='中島 誉也' if not en else 'Takaya Nakashima'
 profile_meta=[('所属','長崎大学病院 麻酔集中治療部','臨床研究センター 助手'),('大学院','長崎大学大学院 医歯薬学総合研究科','麻酔集中治療 博士課程'),('共同研究','TXP Medical',''),('資格・使用言語','統計検定 準1級','R・Python')] if not en else [('Affiliation','Nagasaki University Hospital','Anesthesiology & Intensive Care / Clinical Research Center'),('Graduate program','Nagasaki University','Doctoral program in Anesthesiology & Intensive Care Medicine'),('Collaboration','TXP Medical',''),('Skills','JSS Certificate, Grade Pre-1','R and Python')]
 meta=''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}{f"<small>{esc(c)}</small>" if c else ""}</dd></div>' for a,b,c in profile_meta)
 awards=''.join(f'<li><span>{esc(a["date"])}</span><div><h3>{link(a["href"],esc(a["title"])) if a.get("href") else esc(a["title"])}</h3><p>{esc(a["org"])}</p><p>{esc(a["desc"])}</p></div></li>' for a in d['awards'])
 societies=''.join(f'<li>{esc(x["name"])} <span>{esc(x["since"])}</span></li>' for x in d['societies'])
 themes=''.join(f'<div class="research-row"><span class="theme-no">0{i+1}</span><h4>{esc(x["title"])}</h4><p>{esc(x["body"])}</p></div>' for i,x in enumerate(cp['researchThemes']))
 worklinks=['https://app.j-ka.or.jp/#/dashboard','https://researchmap.jp/nakataka8228/presentations/55017365']
 works=''.join(f'<article><span class="eyebrow">{"WEB APPLICATION" if i==0 else "RESEARCH TOOL"}</span><h4>{esc(x["title"])}</h4><p>{esc(x["body"])}</p>{link(worklinks[i],"詳細を見る" if not en else "View project")}</article>' for i,x in enumerate(cp['works']))
 keywords=''.join(f'<li>{esc(x)}</li>' for x in d['keywords'])
 notes=''.join(f'<li><a href="{esc(x["href"])}" target="_blank" rel="noopener noreferrer"><span class="note-date">{esc(x["date"])}</span><h4 lang="{text_lang(x["title"])}">{esc(x["title"].replace(" — ","：" if not en else ": "))}</h4><span aria-hidden="true">↗</span></a></li>' for x in d['notes'])
 publication_blocks=[]
 publication_links=[]
 for record_type, anchor, labels in [
  ('journal_article','papers',('原著論文','Original articles')),
  ('correspondence','letters',('レター・Correspondence','Letters and correspondence')),
  ('correction','corrections',('訂正記事','Corrections')),
  ('conference_abstract','abstracts',('学会抄録','Conference abstracts')),
  ('preprint','preprints',('プレプリント','Preprints')),
 ]:
  included_types = {'correspondence', 'letter'} if record_type == 'correspondence' else {record_type}
  rows=[(y,p) for y,p in all_papers if p.get('type') in included_types]
  if not rows: continue
  heading=labels[en]
  publication_links.append(f'<li><a href="#{anchor}"><span>{esc(heading)}</span><span class="index-count">{len(rows)}</span></a></li>')
  if record_type=='journal_article':
   latest_year=max(y for y,p in rows)
   recent=[(y,p) for y,p in rows if y==latest_year]
   earlier=[(y,p) for y,p in rows if y!=latest_year]
   body=publication_groups(recent,lang)
   if earlier:
    label=f'過去の原著論文を見る（{len(earlier)}件）' if not en else f'Earlier original articles ({len(earlier)})'
    body+=f'<details class="disclosure"><summary><span>{esc(label)}</span><span class="plus" aria-hidden="true"></span></summary>{publication_groups(earlier,lang)}</details>'
  else:
   body=publication_groups(rows,lang)
  back_label='業績目次へ' if not en else 'Publication index'
  publication_blocks.append(f'<div class="publications" id="{anchor}"><div class="subsection-head publication-heading"><h3>{esc(heading)} <small>{len(rows)}</small></h3><a href="#publications">{back_label}</a></div>{body}</div>')
 publications_html=''.join(publication_blocks)
 publication_index=f'''<nav class="publication-index" id="publications" aria-labelledby="pub-index-title">
  <div class="index-heading"><h3 id="pub-index-title">{"研究業績の目次" if not en else "Publication index"}</h3>{link(SCHOLAR, "Google Scholar", "index-source")}</div>
  <ul>{''.join(publication_links)}</ul>
 </nav>'''
 review_heading='学術誌の査読' if not en else 'Peer review service'
 review_items=''.join(f'<li>{esc(x["journal"])} <span>{esc(x["years"])}</span></li>' for x in CV.get('peer_review_service',[]))
 service_html=f'<div class="works"><div class="subsection-head"><h3>{review_heading}</h3></div><ul class="society-list">{review_items}</ul></div>' if review_items else ''
 cv_update=f'英文CV更新日：{UPDATED.year}年{UPDATED.month}月{UPDATED.day}日' if not en else f'Academic CV updated {UPDATED.day} {UPDATED:%B %Y}'
 html_doc=f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>try {{ if (!matchMedia('(prefers-reduced-motion: reduce)').matches && localStorage.getItem('portfolio-motion') !== 'paused') document.documentElement.classList.add('hero-motion'); }} catch (_) {{}}</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(cp['heroLead'])}">
<meta name="google-site-verification" content="hvCwo7Q3kKA7HeCOFgV9Li-8ylirtfjILbhXgrMBvk4">
<link rel="canonical" href="https://nakashimatakaya.github.io{hreflang}">
<link rel="alternate" hreflang="ja" href="https://nakashimatakaya.github.io/">
<link rel="alternate" hreflang="en" href="https://nakashimatakaya.github.io/en/">
<link rel="alternate" hreflang="x-default" href="https://nakashimatakaya.github.io/en/">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(cp['heroLead'])}">
<meta property="og:type" content="profile">
<meta property="og:url" content="https://nakashimatakaya.github.io{hreflang}">
<meta property="og:image" content="https://nakashimatakaya.github.io/portrait.jpg">
<meta name="theme-color" content="#6a1b33">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600&family=Noto+Serif+JP:wght@500&family=DM+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css?v=20261127b">
<script defer src="{base}site.js?v=20261127"></script>
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'Person','name':'中島誉也','alternateName':'Takaya Nakashima','jobTitle':'Anesthesiologist and Biostatistician','url':'https://nakashimatakaya.github.io/','image':'https://nakashimatakaya.github.io/portrait.jpg','worksFor':{'@type':'Organization','name':'Nagasaki University Hospital'},'sameAs':[SCHOLAR,'https://researchmap.jp/nakataka8228',LINKEDIN,'https://orcid.org/0009-0001-4214-3945','https://github.com/nakashimatakaya']},ensure_ascii=False)}</script>
</head>
<body>
<div class="scroll-progress" aria-hidden="true"></div>
<a class="skip-link" href="#main">{'本文へ' if not en else 'Skip to content'}</a>
<header class="site-header">
 <div class="header-inner">
  <a class="brand" href="#top"><span>{author}</span><small lang="{"ja" if en else "en"}">{"中島 誉也" if en else "TAKAYA NAKASHIMA"}</small></a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav"><span>{'メニュー' if not en else 'Menu'}</span><i aria-hidden="true"></i></button>
  <nav id="site-nav" aria-label="{'メインナビゲーション' if not en else 'Main navigation'}">{''.join(f'<a href="#{a}">{b}</a>' for a,b in nav)}<a class="nav-contact" href="#contact">{'お問い合わせ' if not en else 'Contact'}</a></nav>
  <nav class="language" aria-label="Language">{switch}</nav><button class="motion-toggle" type="button" aria-pressed="false" aria-label="{"Motion" if en else "動き"}" hidden><span aria-hidden="true">Ⅱ</span><span class="motion-label">{"Motion" if en else "動き"}</span></button>
 </div>
</header>
<main id="main">
<section class="hero" id="top">
 <div class="hero-inner container">
  <div class="hero-copy">
   <p class="eyebrow">ANESTHESIOLOGY <span>·</span> BIOSTATISTICS</p>
   <h1>{hero}</h1>
   <p class="hero-name">{author}<span>{'麻酔科医・生物統計家' if not en else 'M.D. / Anesthesiologist & Biostatistician'}</span></p>
   <p class="hero-lead">{esc(cp['heroLead'])}</p>
   <div class="hero-links"><a class="button" href="#selected-research">{'代表研究を見る' if not en else 'Selected research'}<span aria-hidden="true">↓</span></a><a class="quiet-link" href="{base}Takaya_Nakashima_CV.pdf?v={CV["updated_iso"]}" target="_blank" rel="noopener noreferrer">{'英文CV（PDF）' if not en else 'Academic CV (PDF)'}<span aria-hidden="true">↗</span></a></div>
  </div>
  <figure class="hero-photo"><img src="{base}portrait.jpg" alt="{'中島誉也のポートレート' if not en else 'Portrait of Takaya Nakashima'}" width="1968" height="1968" fetchpriority="high"><figcaption>NAGASAKI, JAPAN</figcaption></figure>
 </div>
 <nav class="hero-index container" aria-label="{'業績の概要' if not en else 'Portfolio index'}">
  <a href="#publications"><strong>{len(papers)}</strong><span>{'査読論文' if not en else 'Peer-reviewed papers'}</span></a>
  <a href="#writing"><strong>{len(writings)}</strong><span>{'執筆・翻訳' if not en else 'Writing & translation'}</span></a>
  <a href="#talks"><strong>{len(d['talks'])}</strong><span>{'講演・発表' if not en else 'Talks & presentations'}</span></a>
 </nav>
</section>
<aside class="news"><div class="container"><span class="eyebrow">{esc(news['label'])}</span><span class="news-date">{esc(news['date'])}</span><a href="{esc(news['href'])}" target="_blank" rel="noopener noreferrer">{esc(news['title'])}<span aria-hidden="true">↗</span></a></div></aside>
<section class="section container" id="profile">
 {section_head('01','PROFILE','プロフィール' if not en else 'About me')}
 <div class="profile-grid"><div class="profile-copy"><h3>{author}<span>{'Takaya Nakashima, M.D.' if not en else 'Nagasaki University Hospital'}</span></h3><p>{esc(cp['profileIntro'])}</p><p>{esc(cp['profileBody'])}</p><p>{esc(cp['profileResearch'])}</p><div class="inline-links">{link('https://researchmap.jp/nakataka8228','researchmap')}{link(LINKEDIN,'LinkedIn')}{link(SCHOLAR,'Google Scholar')}{link('https://orcid.org/0009-0001-4214-3945','ORCID')}<a class="text-link" href="{base}Takaya_Nakashima_CV.pdf?v={CV["updated_iso"]}" target="_blank" rel="noopener noreferrer">CV (PDF)<span aria-hidden="true">↗</span></a></div><p class="cv-updated">{esc(cv_update)}</p></div><dl class="profile-facts">{meta}</dl></div>
 <details class="disclosure profile-details" id="awards"><summary><span>{'受賞・所属学会' if not en else 'Awards & memberships'}</span><span aria-hidden="true" class="plus"></span></summary><div class="award-grid"><ol class="award-list">{awards}</ol><div><h3>{'所属学会' if not en else 'Memberships'}</h3><ul class="society-list">{societies}</ul></div></div></details>
</section>
<section class="section research-section" id="research"><div class="container">
 {section_head('02','RESEARCH','研究と論文' if not en else 'Research & publications',cp['researchIntro'])}
 {publication_index}
 <div class="selected-research" id="selected-research"><div class="subsection-head"><h3>{'代表研究' if not en else 'Selected research'}</h3></div><p class="selected-intro">{esc(R[lang]['intro'])}</p>{''.join(selected_study(x,lang).replace('<article ', '<article data-reveal ',1) if i==0 else selected_study(x,lang) for i,x in enumerate(R[lang]['items']))}</div>
 <div class="subsection-head methods-heading"><h3>{'研究領域と解析方法' if not en else 'Research focus & methods'}</h3></div>
 <div class="research-themes">{themes}</div>
 <div class="keyword-area"><h3>RESEARCH KEYWORDS</h3><ul>{keywords}</ul></div>
 {publications_html}
 <div class="works" id="works"><div class="subsection-head"><h3>{'開発・制作' if not en else 'Tools & applications'}</h3><span>PROJECTS</span></div><div class="work-grid">{works}</div></div>
</div></section>
<section class="section container" id="writing">
 {section_head('03','WRITING','執筆と発信' if not en else 'Writing & articles',cp['writingIntro'])}
 <ol class="record-list writing-list">{''.join(record(w,lang,'writing') for w in writings[:4])}</ol><details class="disclosure"><summary><span>{'これまでの執筆・翻訳を見る' if not en else 'Earlier writing & translation'}</span><span class="plus" aria-hidden="true"></span></summary><ol class="record-list">{''.join(record(w,lang,'writing') for w in writings[4:])}</ol></details>
 <div class="notes" id="note"><div class="subsection-head"><h3>note</h3>{link('https://note.com/nakashima_takaya','記事一覧' if not en else 'All articles')}</div><ul>{notes}</ul></div>
</section>
<section class="section talks-section" id="talks"><div class="container">
 {section_head('04','TALKS','講演・学会発表' if not en else 'Talks & presentations')}
 {talk_archive(d['talks'],lang)}
</div></section>
<section class="section container" id="teaching">
 {section_head('05','TEACHING','担当授業・講座' if not en else 'Teaching',cp['teachingIntro'])}
 <ol class="record-list teaching-list">{''.join(record(x,lang,'teaching') for x in d['teaching'])}</ol>{service_html}
</section>
<section class="contact-section" id="contact"><div class="container contact-grid" data-reveal><div><p class="eyebrow">CONTACT</p><h2>{'研究や仕事の<br>ご相談について' if not en else 'Get in touch'}</h2><p>{esc(cp['contactBody'])}</p></div><div class="contact-links"><a class="email" href="mailto:takaya.nakashima@nagasaki-u.ac.jp">takaya.nakashima<span>@nagasaki-u.ac.jp</span><i aria-hidden="true">↗</i></a><div class="inline-links">{link('https://researchmap.jp/nakataka8228','researchmap')}{link(LINKEDIN,'LinkedIn')}{link(SCHOLAR,'Google Scholar')}{link('https://x.com/naka_takaya','X')}{link('https://note.com/nakashima_takaya','note')}</div></div></div></section>
</main>
<footer class="container site-footer"><a class="footer-name" href="#top">TAKAYA NAKASHIMA</a><p>© 2026 Takaya Nakashima</p><a href="#top">{'ページ上部へ' if not en else 'Back to top'} ↑</a></footer>
</body>
</html>'''
 path=ROOT/'en/index.html' if en else ROOT/'index.html';path.parent.mkdir(exist_ok=True,parents=True);path.write_text(html_doc,encoding='utf-8')
print('Built Japanese and English static pages')
