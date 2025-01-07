# LLMを使ったスケジュール調整ツール

## これはなに？

```
以下の時間の中で30分ほどご都合の良い時間はありませんでしょうか？
    10月 28日 (月曜日)⋅13:00～14:00、15:00～16:00
    10月 29日 (火曜日)⋅16:00～17:00
    10月 31日 (木曜日)⋅13:00～14:00
```
といった感じの自然言語の日程候補の文章をもらったときに、GPTで解析して、Googleカレンダーをみて、空いている時間を検索するWebツール

#### 画面イメージ

![img.png](doc/img.png)

#### 紹介ページ

https://qiita.com/fetaro/items/a0894c523e9816c4ecf7

## 使い方

Googleカレンダーの認証情報やOpenAIのAPIキーを入手し配置。

src/conf.py を src/conf_sample.py を参考につくる。

ryeを使って依存ライブラリのインストール

```
rye sync
```

以下のコマンドでStreamlitのWeb画面を起動

```
cd src
streamlit run main.py
```