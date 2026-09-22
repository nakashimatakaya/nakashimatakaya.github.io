from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parent.parent
D=json.loads((ROOT/'data/content.json').read_text())
C=json.loads((ROOT/'data/copy.json').read_text())
esc=lambda s:html.escape(str(s),quote=True)
def link(url,label,cls='text-link'):
 return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label}<span aria-hidden="true">↗</span></a>'
def section_head(n,label,title,intro=''):
 return f'<div class="section-head"><div class="eyebrow"><span>{n}</span>{label}</div><h2>{title}</h2>{f"<p class=section-intro>{esc(intro)}</p>" if intro else ""}</div>'
def record(x,lang,kind='talk'):
 meta=esc(x['meta']).replace(' ／ ',' · ').replace('／ ',' · ')
 label='詳細を見る' if lang=='ja' else 'View details'
 tag=esc(x['tag']);title=esc(x['title']);date=esc(x['date'])
 if x.get('href'): title=f'<a href="{esc(x["href"])}" target="_blank" rel="noopener noreferrer">{title}<span class="record-arrow" aria-hidden="true">↗</span></a>'
 desc=f'<p>{esc(x["description"])}</p>' if x.get('description') else ''
 return f'<li class="record {"upcoming" if x.get("upcoming") else ""}"><div class="record-date"><span>{date}</span><small>{tag}</small></div><div class="record-body"><h3>{title}</h3><p class="record-meta">{meta}</p>{desc}</div></li>'
def paper(p,year,lang):
 role=('筆頭著者' if lang=='ja' else 'First author') if p.get('first') else ('共同筆頭著者' if lang=='ja' else 'Co-first author') if p.get('coFirst') else ''
 authors=esc(p['authorsPre'])+f'<strong>{esc(p["me"])}</strong>'+esc(p['authorsPost'])
 return f'<li class="paper"><div class="paper-meta"><span>{year}</span><span>{esc(p["venue"])}</span>{f"<span>{role}</span>" if role else ""}</div><h3><a href="{esc(p["href"])}" target="_blank" rel="noopener noreferrer">{esc(p["title"])}<span class="record-arrow" aria-hidden="true">↗</span></a></h3><p class="authors">{authors}</p></li>'
for lang in ['ja','en']:
 en=lang=='en';d=D[lang];cp=C[lang];base='../' if en else './'
 writings=d['writings']
 papers=[(g['year'],p) for g in d['pubYears'] for p in g['items']]
 nav=[('profile','Profile' if en else 'プロフィール'),('research','Research' if en else '研究・論文'),('writing','Writing' if en else '執筆・発信'),('talks','Talks' if en else '講演'),('teaching','Teaching' if en else '教育')]
 title='Takaya Nakashima | Clinical care and statistics' if en else '中島誉也 | 臨床と統計の橋渡しを。'
 hero='Bridging<br>clinical care<br>and <em>statistics.</em>' if en else '臨床と統計の<br><em>橋渡し</em>を。'
 hreflang='/en/' if en else '/'
 switch='<a href="../" lang="ja">日本語</a><span aria-current="page">EN</span>' if en else '<span aria-current="page">JA</span><a href="./en/" lang="en">EN</a>'
 upcoming=d['talks'][0]
 author='中島 誉也' if not en else 'Takaya Nakashima'
 profile_meta=[('所属','長崎大学病院 麻酔集中治療部','臨床研究センター 助手'),('大学院','長崎大学大学院 医歯薬学総合研究科','麻酔集中治療 博士課程'),('共同研究','TXP Medical',''),('資格・使用言語','統計検定 準1級','R・Python')] if not en else [('Affiliation','Nagasaki University Hospital','Anesthesiology & Intensive Care / Clinical Research Center'),('Graduate program','Nagasaki University','Doctoral program in Anesthesiology & Intensive Care Medicine'),('Collaboration','TXP Medical',''),('Skills','JSS Certificate, Grade Pre-1','R and Python')]
 meta=''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}{f"<small>{esc(c)}</small>" if c else ""}</dd></div>' for a,b,c in profile_meta)
 awards=''.join(f'<li><span>{esc(a["date"])}</span><div><h3>{esc(a["title"])}</h3><p>{esc(a["org"])}</p><p>{esc(a["desc"])}</p></div></li>' for a in d['awards'])
 societies=''.join(f'<li>{esc(x["name"])} <span>{esc(x["since"])}</span></li>' for x in d['societies'])
 themes=''.join(f'<div class="research-row"><span class="theme-no">0{i+1}</span><h3>{esc(x["title"])}</h3><p>{esc(x["body"])}</p></div>' for i,x in enumerate(cp['researchThemes']))
 worklinks=['https://app.j-ka.or.jp/#/dashboard','https://researchmap.jp/nakataka8228/published_papers/43860537']
 works=''.join(f'<article><span class="eyebrow">{"WEB APPLICATION" if i==0 else "RESEARCH TOOL"}</span><h3>{esc(x["title"])}</h3><p>{esc(x["body"])}</p>{link(worklinks[i],"詳細を見る" if not en else "View project")}</article>' for i,x in enumerate(cp['works']))
 keywords=''.join(f'<li>{esc(x)}</li>' for x in d['keywords'])
 notes=''.join(f'<li><a href="{esc(x["href"])}" target="_blank" rel="noopener noreferrer"><span class="note-date">{esc(x["date"])}</span><h3>{esc(x["title"].replace(" — ","：" if not en else ": "))}</h3><span aria-hidden="true">↗</span></a></li>' for x in d['notes'])
 upcoming_label='登壇予定' if not en else 'Upcoming talk'
 heading_papers='論文' if not en else 'Publications'
 html_doc=f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(cp['heroLead'])}">
<meta name="google-site-verification" content="hvCwo7Q3kKA7HeCOFgV9Li-8ylirtfjILbhXgrMBvk4">
<link rel="canonical" href="https://nakashimatakaya.github.io{hreflang}">
<link rel="alternate" hreflang="ja" href="https://nakashimatakaya.github.io/">
<link rel="alternate" hreflang="en" href="https://nakashimatakaya.github.io/en/">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(cp['heroLead'])}">
<meta property="og:type" content="profile">
<meta property="og:url" content="https://nakashimatakaya.github.io{hreflang}">
<meta property="og:image" content="https://nakashimatakaya.github.io/portrait.jpg">
<meta name="theme-color" content="#641f37">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@400;500;600&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css?v=20260922e">
<script defer src="{base}site.js?v=20260922e"></script>
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'Person','name':'中島誉也','alternateName':'Takaya Nakashima','jobTitle':'Anesthesiologist and Biostatistician','url':'https://nakashimatakaya.github.io/','image':'https://nakashimatakaya.github.io/portrait.jpg','worksFor':{'@type':'Organization','name':'Nagasaki University Hospital'},'sameAs':['https://researchmap.jp/nakataka8228','https://orcid.org/0009-0001-4214-3945','https://github.com/nakashimatakaya']},ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">{'本文へ' if not en else 'Skip to content'}</a>
<header class="site-header">
 <div class="header-inner">
  <a class="brand" href="#top"><span>{author}</span><small>TAKAYA NAKASHIMA</small></a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav"><span>{'メニュー' if not en else 'Menu'}</span><i aria-hidden="true"></i></button>
  <nav id="site-nav" aria-label="{'メインナビゲーション' if not en else 'Main navigation'}">{''.join(f'<a href="#{a}">{b}</a>' for a,b in nav)}<a class="nav-contact" href="#contact">{'お問い合わせ' if not en else 'Contact'}</a></nav>
  <div class="language" aria-label="Language">{switch}</div>
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
   <div class="hero-links"><a class="button" href="#research">{'研究・論文を見る' if not en else 'Explore my research'}<span aria-hidden="true">↗</span></a><a class="quiet-link" href="#profile">{'プロフィール' if not en else 'About me'}<span aria-hidden="true">↓</span></a></div>
  </div>
  <figure class="hero-photo"><img src="{base}portrait.jpg" alt="{'中島誉也のポートレート' if not en else 'Portrait of Takaya Nakashima'}" width="1968" height="1968" fetchpriority="high"><figcaption>NAGASAKI, JAPAN</figcaption></figure>
 </div>
 <div class="hero-bottom container"><p>CLINICAL CARE<br>AND RESEARCH</p><dl><div><dt>{'論文' if not en else 'Publications'}</dt><dd>{len(papers)}</dd></div><div><dt>{'執筆・翻訳' if not en else 'Writing & translation'}</dt><dd>{len(writings)}</dd></div><div><dt>{'講演・学会発表' if not en else 'Talks & presentations'}</dt><dd>{sum(not x.get('upcoming') for x in d['talks'])}</dd></div><div><dt>{'受賞' if not en else 'Awards'}</dt><dd>{len(d['awards'])}</dd></div></dl><a href="#profile" class="scroll-cue">SCROLL <span>↓</span></a></div>
</section>
<aside class="news"><div class="container"><span class="eyebrow">{upcoming_label}</span><span class="news-date">2026.10.13</span><a href="#talks">{'SASユーザー総会2026 Day0で生成AIと統計解析について発表します' if not en else 'Generative AI and statistical analysis at SAS User Meeting 2026, Day 0'}<span aria-hidden="true">↗</span></a></div></aside>
<section class="section container" id="profile">
 {section_head('01','PROFILE','プロフィール' if not en else 'About me')}
 <div class="profile-grid"><div class="profile-copy"><h3>{author}<span>{'Takaya Nakashima, M.D.' if not en else 'Nagasaki University Hospital'}</span></h3><p>{esc(cp['profileIntro'])}</p><p>{esc(cp['profileBody'])}</p><div class="inline-links">{link('https://researchmap.jp/nakataka8228','researchmap')}{link('https://orcid.org/0009-0001-4214-3945','ORCID')}<a class="text-link" href="{base}Takaya_Nakashima_CV.pdf" target="_blank">CV (PDF)<span>↗</span></a></div></div><dl class="profile-facts">{meta}</dl></div>
 <details class="disclosure profile-details" id="awards"><summary><span>{'受賞・所属学会' if not en else 'Awards & memberships'}</span><span aria-hidden="true" class="plus"></span></summary><div class="award-grid"><ol class="award-list">{awards}</ol><div><h3>{'所属学会' if not en else 'Memberships'}</h3><ul class="society-list">{societies}</ul></div></div></details>
</section>
<section class="section research-section" id="research"><div class="container">
 {section_head('02','RESEARCH','研究と論文' if not en else 'Research & publications',cp['researchIntro'])}
 <div class="research-themes">{themes}</div>
 <div class="keyword-area"><h3>RESEARCH KEYWORDS</h3><ul>{keywords}</ul></div>
 <div class="publications" id="papers"><div class="subsection-head"><h3>{heading_papers}</h3><span>12 PUBLICATIONS</span></div><ol class="paper-list">{''.join(paper(p,y,lang) for y,p in papers[:3])}</ol><details class="disclosure"><summary><span>{'2021〜2025年の論文を見る（9件）' if not en else 'Earlier publications, 2021–2025 (9)'}</span><span class="plus" aria-hidden="true"></span></summary><ol class="paper-list">{''.join(paper(p,y,lang) for y,p in papers[3:])}</ol></details></div>
 <div class="works" id="works"><div class="subsection-head"><h3>{'開発・制作' if not en else 'Tools & applications'}</h3><span>PROJECTS</span></div><div class="work-grid">{works}</div></div>
</div></section>
<section class="section container" id="writing">
 {section_head('03','WRITING','執筆と発信' if not en else 'Writing & articles',cp['writingIntro'])}
 <ol class="record-list writing-list">{''.join(record(w,lang,'writing') for w in writings[:4])}</ol><details class="disclosure"><summary><span>{'これまでの執筆・翻訳を見る' if not en else 'Earlier writing & translation'}</span><span class="plus" aria-hidden="true"></span></summary><ol class="record-list">{''.join(record(w,lang,'writing') for w in writings[4:])}</ol></details>
 <div class="notes" id="note"><div class="subsection-head"><h3>note</h3>{link('https://note.com/nakashima_takaya','記事一覧' if not en else 'All articles')}</div><ul>{notes}</ul></div>
</section>
<section class="section talks-section" id="talks"><div class="container">
 {section_head('04','TALKS','講演・学会発表' if not en else 'Talks & presentations')}
 <p class="section-caption">{'発表済み8件・登壇予定1件' if not en else '8 presentations delivered · 1 scheduled'}</p>
 <ol class="record-list">{''.join(record(x,lang) for x in d['talks'][:4])}</ol><details class="disclosure"><summary><span>{'過去の学会発表を見る（5件）' if not en else 'Earlier presentations (5)'}</span><span class="plus" aria-hidden="true"></span></summary><ol class="record-list">{''.join(record(x,lang) for x in d['talks'][4:])}</ol></details>
</div></section>
<section class="section container" id="teaching">
 {section_head('05','TEACHING','担当授業・講座' if not en else 'Teaching',cp['teachingIntro'])}
 <ol class="record-list teaching-list">{''.join(record(x,lang,'teaching') for x in d['teaching'])}</ol>
</section>
<section class="contact-section" id="contact"><div class="container contact-grid"><div><p class="eyebrow">CONTACT</p><h2>{'研究や仕事の<br>ご相談について' if not en else 'Let’s work<br>together.'}</h2><p>{esc(cp['contactBody'])}</p></div><div class="contact-links"><a class="email" href="mailto:takaya.nakashima@nagasaki-u.ac.jp">takaya.nakashima<span>@nagasaki-u.ac.jp</span><i aria-hidden="true">↗</i></a><div class="inline-links">{link('https://researchmap.jp/nakataka8228','researchmap')}{link('https://x.com/naka_takaya','X')}{link('https://note.com/nakashima_takaya','note')}</div></div></div></section>
</main>
<footer class="container site-footer"><a class="footer-name" href="#top">TAKAYA NAKASHIMA</a><p>© 2026 Takaya Nakashima</p><a href="#top">{'ページ上部へ' if not en else 'Back to top'} ↑</a></footer>
</body>
</html>'''
 path=ROOT/'en/index.html' if en else ROOT/'index.html';path.parent.mkdir(exist_ok=True,parents=True);path.write_text(html_doc)
print('Built Japanese and English static pages')
