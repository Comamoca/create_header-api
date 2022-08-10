<div align="center">

![Last commit](https://img.shields.io/github/last-commit/Comamoca/create_header-api?style=flat-square)
![Repository Stars](https://img.shields.io/github/stars/Comamoca/create_header-api?style=flat-square)
![Issues](https://img.shields.io/github/issues/Comamoca/create_header-api?style=flat-square)
![Open Issues](https://img.shields.io/github/issues-raw/Comamoca/create_header-api?style=flat-square)
![Bug Issues](https://img.shields.io/github/issues/Comamoca/create_header-api/bug?style=flat-square)

# 🦊 header-maker-api

これはHeaderMakerのバックエンドサーバーです。

</div>

<table>
  <thead>
    <tr>
      <th style="text-align:center">🍡日本語</th>
      <th style="text-align:center"><a href="README.md">Japanease Only</a></th>
    </tr>
  </thead>
</table>

<div align="center">

</div>

## 🚀 使い方

```sh
poetry install
poetry run uvicorn src.server:app --reload
```

上記のコマンドでサーバーを起動したあと、`http://localhost:8000/docs`にアクセスするとSwaggerドキュメントが見られます。

## ⬇️  Install

Windows、Linux、Macの各OSのインストール方法を書いてみましょう。
Linuxディストリビューションごとにインストール方法を書くと更に良いでしょう。

バイナリで配布する場合は、リリースページについても書いてください。

また、ソースからインストールする方法についても書いてください。

## ⛏️   開発

```sh
poetry run uvicorn src.server:app --host 0.0.0.0 --reload
```

## 📝 Todo

- [ ] リファクタリング
- [ ] APIの拡充
- [ ] フロントとの連携強化

## 📜 ライセンス

オープンソースにおいてライセンスは重要です。必ず書くようにしましょう。

### 🧩 Modules

Pillow

## 👏 影響を受けたプロジェクト

Haiku

## 💕 スペシャルサンクス

poetry
pillow
