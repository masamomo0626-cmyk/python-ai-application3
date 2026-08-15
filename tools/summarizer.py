import streamlit as st
from utils.gemini import generate

def render():
    st.header("📋 文章要約")
    st.caption("長文を入力すると、指定した形式・長さで要約します。")

    text = st.text_area("要約したい文章", placeholder="ここに要約したい文章を貼り付けてください...", height=250)

    col1, col2 = st.columns(2)
    with col1:
        format_type = st.selectbox("要約の形式", [
            "箇条書き（ポイントをまとめる）",
            "文章形式（流れをそのまま短く）",
            "一言要約（ひと言でまとめる）",
        ])
    with col2:
        summary_length = st.selectbox("要約の長さ", [
            "超短く（50字以内）",
            "短め（100〜150字）",
            "普通（200〜300字）",
            "長め（400〜500字）",
        ])

    focus = st.text_input("特に重視してほしいポイント", placeholder="例：結論・数値・課題点を重点的に")

    if st.button("要約する", type="primary", use_container_width=True):
        if not text:
            st.warning("要約したい文章を入力してください。")
            return

        length_map = {
            "超短く（50字以内）": "50文字以内",
            "短め（100〜150字）": "100〜150文字",
            "普通（200〜300字）": "200〜300文字",
            "長め（400〜500字）": "400〜500文字",
        }

        prompt = f"""以下の文章を要約してください。

【要約する文章】
{text}

【要約の形式】{format_type}
【要約の長さ】{length_map[summary_length]}
【重視するポイント】{focus or "なし（全体をバランスよく）"}

要約のみを出力し、前置きや説明文は不要です。"""

        with st.spinner("要約中..."):
            try:
                result = generate(prompt)
                st.success("要約完了！")
                st.markdown("---")

                original_chars = len(text)
                summary_chars = len(result)
                ratio = int((1 - summary_chars / original_chars) * 100) if original_chars > 0 else 0

                col_a, col_b, col_c = st.columns(3)
                col_a.metric("元の文字数", f"{original_chars:,} 字")
                col_b.metric("要約後の文字数", f"{summary_chars:,} 字")
                col_c.metric("圧縮率", f"{ratio}% 削減")

                st.markdown("### 要約結果")
                st.info(result)
                st.download_button(
                    "📥 テキストとしてダウンロード",
                    data=result,
                    file_name="summary.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
