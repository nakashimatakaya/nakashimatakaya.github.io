# 中島誉也の個人サイト

GitHub Pagesで公開する日英の静的サイト。

- `index.html`：日本語ページ
- `en/index.html`：英語ページ
- `style.css`：共通スタイル
- `site.js`：モバイルメニューとアンカー操作
- `data/content.json`：業績・リンク・日付
- `data/copy.json`：プロフィールなどの紹介文
- `scripts/build.py`：日英HTMLの生成
- `portrait.jpg`：プロフィール写真（1968×1968px）
- `portrait.png`：旧URLとの互換用に残す写真
- `Takaya_Nakashima_CV.pdf`：ダウンロード用CV

## 更新

`data/`のJSONを編集し、リポジトリ内で次を実行する。

```sh
python3 scripts/build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

`http://127.0.0.1:8765/`と`/en/`で表示を確認する。生成されたHTMLもコミットし、`main`へpushするとGitHub Pagesから公開される。

本文と業績はJavaScriptがなくても読める。CSS・JavaScriptを変更したときは、`scripts/build.py`の読み込みURLに付けた`v`を更新してから再生成する。

## 記録上の扱い

- SASユーザー総会2026の登壇は予定。実施済みの発表件数には含めない。
- mJOHNSNOWの担当年月は未確認のため掲載していない。
- 「Gen AI時代のタイパ・コスパ論文執筆術」は医学書院の[公式連載一覧](https://www.igaku-shoin.co.jp/paperplus/series/00001)に基づき、全10回のWeb連載1件として掲載する。旧サイトの同名の書籍項目と連載項目を統合した。
- 正式な論文名・演題名は維持し、紹介文とは分けて管理する。

## プロフィール写真

2026年9月22日、[本人のnoteプロフィール](https://note.com/nakashima_takaya)で使用している1968×1968pxの[写真](https://assets.st-note.com/production/uploads/images/270214564/profile_095395a14bd3b164e9ff2fb7e5a4830f.png)へ差し替えた。配信元URLはpng表記だがファイル形式はJPEGのため、`portrait.jpg`として保存。画像の加工・再圧縮は行っていない。
