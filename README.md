# logistic-data-app

[![Join the chat at https://gitter.im/suitai/logistic-data-app](https://badges.gitter.im/suitai/logistic-data-app.svg)](https://gitter.im/suitai/logistic-data-app?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[フレームワークス物流オープンデータ活用コンテスト](http://contest.frameworxopendata.jp/)
向けのアプリです。

# Description

その日の仕事量(ピッキングした商品数)、カロリー消費量、歩数、移動距離、
を確認したり、他の人と比較したりできる Web アプリです。

## アプリ説明

1 日のうちでどれくらい働いたのか、確認できる作業ログページと、
他の人と比べてどれくらい働いたのか、確認できるランキングページがあります。

### 作業ログページ

作業ログページでは、以下の 3 つのことができます。

- 1 日のどの時間帯でどれだけ頑張ったのかを線グラフで表示
- 商品数、カロリー消費量、歩数、移動距離をまとめて表示
- 地図上でその日動いた道筋とピッキンギした場所を表示

### ランキングページ

ランキングページでは、商品数、カロリー消費量、歩数、移動距離のランキングを計算して、
各項目の Top 3 と自分の順位、ランキング 1 位との差が表示されます

## 使い方

### MVP 活動

ランキングページを用いて、その日の MVP を決め表彰しましょう。
MVP として表彰されると、日々の仕事のちょっとした励みになるでしょう。
幹部社員の方は、ポケットマネーのご用意を。

### 仕事の効率化

ログページを用いて、日頃の仕事を見直しましょう。
「前半頑張りすぎたから、後半ばててるな」とか、
「ここのピッキングはもう少し効率できるな」などと、
見直してみると、新たな発見があるかもしれません。

# Usage

* Webアプリ用HTTPサーバ起動

```
$ git clone https://github.com/suitai/logistic-data-app.git
$ cd logistic-data-app
$ pip install -r requirements.txt
$ vi app.json    # 設定ファイルの作成
$ python main.py
```

* ES6が動作するブラウザでアクセス
* 適当にフィルタリングするための項目を入力
* 送信ボタンをクリック
* なんかしらの情報を取得できる
