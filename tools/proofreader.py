import streamlit as st
from utils.gemini import generate

def render():
    st.header("✏️ 文章校正・リライト")
    st.caption("文章の誤字脱字・表現の改善・読みやすさの向上を行います。")

    text = st.text_area("校正・改善したい文章", placeholder="ここに文章を入力してください...", height=200)

    mode = st.radio(
        "モードを選択",
        ["校正のみ（誤字脱字・文法チェック）", "表現改善（より自然な表現に）", "全面リライト（内容を保ちつつ全体を書き直す）"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("目標の文体", ["現状維持", "よりフォーマルに", "よりカジュアルに", "より簡潔に", "より丁寧に"])
    with col2:
        show_diff = st.checkbox("変更点を説明してほしい", value=True)

    if st.button("校正・改善する", type="primary", use_container_width=True):
        if not text:
            st.warning("文章を入力してください。")
            return

        explain_instruction = "最後に変更したポイントを箇条書きで説明してください。" if show_diff else "修正後の文章のみ出力してください。"

        prompt = f"""以下の文章を指示に従って改善してください。

【元の文章】
{text}

【モード】{mode}
【目標の文体】{tone}

{explain_instruction}"""

        with st.spinner("処理中..."):
            try:
                result = generate(prompt)
                st.success("完了！")
                st.markdown("---")

                col_orig, col_fixed = st.columns(2)
                with col_orig:
                    st.markdown("**元の文章**")
                    st.text_area("", value=text, height=200, disabled=True, key="original")
                with col_fixed:
                    st.markdown("**改善後の文章**")
                    st.text_area("", value=result, height=200, key="fixed")

                st.download_button(
                    "📥 改善後の文章をダウンロード",
                    data=result,
                    file_name="proofread.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
