import streamlit as st
from utils.gemini import generate

LANGUAGES = ["英語", "日本語", "中国語（簡体字）", "韓国語", "スペイン語", "フランス語", "ドイツ語"]

def render():
    st.header("🌐 翻訳")
    st.caption("文章を入力すると、指定した言語・トーンで自然な翻訳文を生成します。")

    text = st.text_area("翻訳したい文章", placeholder="ここに翻訳したい文章を貼り付けてください...", height=200)

    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox("翻訳先の言語", LANGUAGES)
        tone = st.selectbox("トーン", ["標準・ニュートラル", "ビジネス・フォーマル", "カジュアル・親しみやすい"])
    with col2:
        show_furigana_note = st.checkbox("直訳に近い逐語訳を併記してほしい", value=False)
        notes = st.text_input("その他の指示", placeholder="例：専門用語はそのまま残す")

    if st.button("翻訳する", type="primary", use_container_width=True):
        if not text:
            st.warning("翻訳したい文章を入力してください。")
            return

        extra_instruction = "自然な訳文の後に、直訳に近い逐語訳を「（直訳）」として併記してください。" if show_furigana_note else "自然な訳文のみを出力してください。"

        prompt = f"""以下の文章を{target_lang}に翻訳してください。

【原文】
{text}

【トーン】{tone}
【その他の指示】{notes or "なし"}

{extra_instruction}
訳文以外の説明文は不要です。"""

        with st.spinner("翻訳中..."):
            try:
                result = generate(prompt)
                st.success("翻訳完了！")
                st.markdown("---")
                st.text_area("翻訳結果", value=result, height=250)
                st.download_button(
                    "📥 テキストとしてダウンロード",
                    data=result,
                    file_name="translation.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
