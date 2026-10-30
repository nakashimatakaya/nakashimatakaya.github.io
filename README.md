# 中島誉也の個人サイト

GitHub Pagesで公開する日英の静的サイト。

- `index.html`：日本語ページ
- `en/index.html`：英語ページ
- `style.css`：共通スタイル
- `site.js`：モバイルメニュー、アンカー操作、登場アニメーションと停止操作
- `data/content.json`：業績・リンク・日付・トップのお知らせ
- `data/copy.json`：プロフィールなどの紹介文
- `data/research.json`：日英の代表研究紹介、著者役割、論文・解析コードへのリンク
- `scripts/build.py`：日英HTMLの生成
- `portrait.jpg`：プロフィール写真（1968×1968px）
- `portrait.png`：旧URLとの互換用に残す写真
- `Takaya_Nakashima_CV.pdf`：ダウンロード用CV
- `data/cv.json`：CV用の経歴・学歴・書誌情報
- `scripts/build_cv.py`：英文CVの生成（ReportLabを使用）

## 更新

`data/`のJSONを編集し、リポジトリ内で次を実行する。

```sh
python3 scripts/build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

`http://127.0.0.1:8765/`と`/en/`で表示を確認する。生成されたHTMLもコミットし、`main`へpushするとGitHub Pagesから公開される。

本文と業績はJavaScriptがなくても読める。CSS・JavaScriptを変更したときは、`scripts/build.py`の読み込みURLに付けた`v`を更新してから再生成する。

CVは`data/content.json`の業績と`data/cv.json`から生成する。更新日は`data/cv.json`とページ内のCV更新日を揃える。

```sh
python3 scripts/build_cv.py
```

生成後はPDFの全ページを確認する。`CV_FONT_DIR`でLiberation SansのTTFファイルの配置先を指定できる。

## 記録上の扱い

- SASユーザー総会2026はプログラム掲載内容として記録している。講演・学会発表の件数には、プログラム掲載の発表も含む。
- 2026年10月7日の高知大学での特別講演は、最終案内と[researchmapの登録内容](https://researchmap.jp/nakataka8228/presentations/55321962)に基づく。
- プロフィールと連絡先欄にresearchmap・LinkedInへのリンクを掲載する。LinkedInは本人の公開プロフィールURLを使用する。
- mJOHNSNOWの担当年月は未確認のため掲載していない。
- 「Gen AI時代のタイパ・コスパ論文執筆術」は医学書院の[公式連載一覧](https://www.igaku-shoin.co.jp/paperplus/series/00001)に基づき、全10回のWeb連載1件として掲載する。旧サイトの同名の書籍項目と連載項目を統合した。
- 正式な論文名・演題名は維持し、紹介文とは分けて管理する。
- 代表研究は研究の問いと解析方法を紹介する。ICM論文の責任著者表示と解析コードは[出版社の記載](https://link.springer.com/article/10.1007/s00134-026-08575-3)、乳酸の研究は[International Heart Journalの原著論文](https://doi.org/10.1536/ihj.23-659)に基づく。
- 学位は博士課程在籍として記載する。学位取得日、海外留学の開始時期・受け入れ先など、未確定の予定は掲載しない。
- 2026年10月30日時点の査読論文は12件（Correspondenceを含む）。WebとCVで学会抄録1件を別に掲載する。演題査読と論文査読は区別する。共同筆頭著者4件、責任著者3件。

## プロフィール写真

2026年9月22日、[本人のnoteプロフィール](https://note.com/nakashima_takaya)で使用している1968×1968pxの[写真](https://assets.st-note.com/production/uploads/images/270214564/profile_095395a14bd3b164e9ff2fb7e5a4830f.png)へ差し替えた。配信元URLはpng表記だがファイル形式はJPEGのため、`portrait.jpg`として保存。画像の加工・再圧縮は行っていない。

## 表示と動き

2026年10月30日、Claude Opus 5.5のデザイン提案をもとに共通CSSを更新。暖色の紙色、バーガンディの見出し、オレンジのリンクを使用する。本文はPCで18px、スマートフォンで17px。論文は年別に掲載する。

見出しや写真の登場は1回だけ。ヘッダーの停止ボタンと端末の「視差効果を減らす」設定に対応し、停止状態をブラウザーに保存する。JavaScriptが無効でも本文とナビゲーションを表示する。写真そのものは加工していない。
