# ホームページ（GitHub Pages 用）

臨床と統計の橋渡し — 個人ホームページの静的ファイル一式。

## 構成

```
index.html                    ページ本体
support.js                    描画ランタイム
react.production.min.js       React 18.3.1
react-dom.production.min.js   ReactDOM 18.3.1
portrait.png                  近影
```

フォント（Shippori Mincho B1 / Noto Sans JP / JetBrains Mono）は Google Fonts から読み込む。

## 公開手順

1. GitHub で新しいリポジトリを作成（例: `homepage`）
2. このフォルダの中身をリポジトリの**ルート**にアップロード（`index.html` がルート直下にあること）
3. リポジトリの **Settings → Pages** を開く
4. Source: **Deploy from a branch** / Branch: **main** / フォルダ: **/ (root)** を選んで Save
5. 数分後 `https://<ユーザー名>.github.io/<リポジトリ名>/` で公開される

`<ユーザー名>.github.io` という名前のリポジトリにすれば `https://<ユーザー名>.github.io/` 直下になる。

## 更新

`index.html` を差し替えて push するだけ。

`support.js` には、公開直後に古いキャッシュのテンプレートと新しい表示データが混在しないための修正を加えている。ページの再取得時はキャッシュを使わず、読み込み済みのスクリプトと一致する場合にだけテンプレートを更新する。ランタイムを再生成する際は、この処理を維持すること。`support.js` を変更した場合は、`index.html` の読み込みURLに付けた `v` も更新する。
