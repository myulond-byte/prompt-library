# Prompt Library — セットアップガイド

## ファイル構成

```
WEBプロジェクト/
├── index.html       ← ビューワー本体（このファイル）
├── build.py         ← mdをJSONに変換するスクリプト
├── prompts.json     ← build.py が生成（Gitで管理）
├── AIその他/
│   └── *.md
├── LP制作/
│   └── *.md
└── ...
```

---

## 初回セットアップ

### 1. ファイルを置く
`index.html` と `build.py` を `WEBプロジェクト/` フォルダに置く。

### 2. JSONを生成する
ターミナル（PowerShell / コマンドプロンプト）を開き：

```bash
cd Desktop/WEBプロジェクト
python build.py
```

`prompts.json` が生成されます。

### 3. GitHub にプッシュ

```bash
git add .
git commit -m "update prompts"
git push
```

### 4. GitHub Pages を有効化
リポジトリの Settings → Pages → Source: `main` ブランチの `/ (root)` を選択して Save。

数分後に `https://{ユーザー名}.github.io/{リポジトリ名}/` でスマホからもアクセスできます。

---

## mdファイルの書き方

`## 見出し` または `### 見出し` ごとに1プロンプトとして認識されます。

```markdown
## セールスレター作成

あなたは一流のコピーライターです。
...プロンプト本文...

## ブログ記事構成案

SEOライターとして...
```

見出しがないファイルはファイル全体が1プロンプトになります。

---

## mdを更新したら

```bash
python build.py
git add prompts.json
git commit -m "update prompts"
git push
```

これだけでスマホ側にも即反映されます。
