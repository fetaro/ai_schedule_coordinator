# LLMを使ったスケジュール調整ツール

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