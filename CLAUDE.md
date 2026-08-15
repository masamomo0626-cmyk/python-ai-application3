# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 起動・セットアップ

```bash
pip install -r requirements.txt
streamlit run app.py
```

環境変数は `.env` ファイルで管理（`.env.example` 参照）：
```
GEMINI_API_KEY=your_api_key_here
```

APIキーの動作確認・利用可能モデルの調査は `check_api.py` を使う：
```bash
python check_api.py   # .env の GEMINI_API_KEY を読み込んで実行
```

### 非対話シェル・バックグラウンド起動時の注意（Windows）

Streamlit は初回起動時にオンボーディング用のメールアドレス入力プロンプトを標準入力で待ち受ける。非対話シェルやバックグラウンド実行（`run_in_background` 等）でこれに当たると、入力を受け取れずプロセスが exit code 255 で終了する。

回避するには `%USERPROFILE%\.streamlit\credentials.toml` を事前に作成しておく：
```toml
[general]
email = ""
```
これはユーザーのホームディレクトリ配下の設定であり、プロジェクトの一部ではない（マシン単位で一度作成すれば以降のプロジェクトすべてに有効）。

さらに起動コマンドには `--server.headless true` を付けること：
```bash
streamlit run app.py --server.headless true
```

## アーキテクチャ

**Streamlit マルチツールアプリ**。`app.py` がサイドバーナビゲーションを管理し、選択されたツールの `render()` を呼び出す構造。

```
app.py                  # エントリポイント。TOOLSディクショナリでツールを登録
tools/                  # 各ライティングツール（blog_writer, email_reply, summarizer, proofreader, sns_writer, catchphrase, translator）
utils/gemini.py         # Gemini APIクライアントの唯一の窓口
check_api.py            # APIキー診断用スクリプト（アプリ本体ではない）
```

### ツール追加パターン

新しいツールを追加する場合：
1. `tools/` にファイルを作成し、`render()` 関数を実装する
2. `app.py` の `TOOLS` ディクショナリにエントリを追加する

各ツールは `from utils.gemini import generate` でLLMを呼び出す。UIはStreamlit、出力はすべて日本語。

### 各ツールの特記事項

| ツール | 特徴 |
|--------|------|
| `blog_writer` | マークダウン形式で出力。`st.markdown()` でレンダリング |
| `email_reply` | 日本語・英語の切り替えあり。`st.text_area` で編集可能な形で表示 |
| `summarizer` | 生成後に元文字数・要約後文字数・圧縮率をメトリクス表示 |
| `proofreader` | 元文章と改善後を左右カラムで並べて比較表示 |
| `sns_writer` | **プラットフォームごとに `generate()` を個別呼び出し**（複数選択時はAPI呼び出しが複数回発生）。ループ内の Streamlit ウィジェットに `key=platform` / `key=f"dl_{platform}"` が必要 |
| `catchphrase` | 生成結果を改行で分割してリスト表示。番号付き行を想定したプロンプト設計 |
| `translator` | 翻訳先の言語・トーンを選択式で指定。逐語訳の併記はチェックボックスで切り替え |

### プロンプトの書き方（全ツール共通）

プロンプトは `【パラメータ名】値` の形式で構造化し、末尾に出力形式の指示を入れる：
```
【テーマ】{topic}
【文字数】{length}
...
マークダウン形式で出力してください。説明文は不要です。
```
この形式を新ツール追加時も踏襲すること。

### Gemini APIクライアント（`utils/gemini.py`）

- `google.generativeai`（旧・非推奨）ではなく **`google.genai`**（新）を使用。パッケージ名は `google-genai`
- 使用モデルは `GEMINI_MODEL` 環境変数で制御。デフォルトは `gemini-2.5-flash-lite`
- サイドバーのモデルセレクタが `os.environ["GEMINI_MODEL"]` を上書きし、`generate()` が参照する
- `generate(prompt)` の呼び出しは同期・ストリーミングなし

### モデル選択に関する注意

無料枠のAPIキーではモデルによって 429（クォータ超過）が発生する場合がある。動作しないモデルに遭遇したら `check_api.py` で動作確認済みモデルを再調査し、このファイルに追記すること。

このプロジェクト（python-ai-application, python-ai-application2）で確認された動作実績：
- `gemini-2.5-flash-lite`（推奨デフォルト、安定）
- `gemini-2.5-flash`（高負荷時に503の場合あり）
- `gemini-2.0-flash` 系は free tier クォータ0で動作しない場合がある
