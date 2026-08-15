import streamlit as st
from utils.gemini import generate

def render():
    st.header("📝 ブログ記事執筆")
    st.caption("テーマや条件を入力するだけで、構成付きのブログ記事を生成します。")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("記事のテーマ・タイトル", placeholder="例：初心者向けPythonの始め方")
        target = st.text_input("ターゲット読者", placeholder="例：プログラミング初心者、20〜30代")
    with col2:
        length = st.selectbox("記事の長さ", ["短め（500字程度）", "普通（1000字程度）", "長め（2000字程度）"])
        tone = st.selectbox("文体・トーン", ["親しみやすい・カジュアル", "丁寧・フォーマル", "専門的・論理的"])

    keywords = st.text_input("含めたいキーワード（カンマ区切り）", placeholder="例：Python, 初心者, 環境構築")
    notes = st.text_area("その他の要望・補足", placeholder="例：SEOを意識して、見出しにキーワードを含める", height=80)

    if st.button("記事を生成する", type="primary", use_container_width=True):
        if not topic:
            st.warning("テーマを入力してください。")
            return

        length_map = {
            "短め（500字程度）": "約500文字",
            "普通（1000字程度）": "約1000文字",
            "長め（2000字程度）": "約2000文字",
        }
        prompt = f"""以下の条件でSEOを意識したブログ記事を日本語で執筆してください。

【テーマ】{topic}
【ターゲット読者】{target or "一般的な読者"}
【文字数】{length_map[length]}
【文体・トーン】{tone}
【キーワード】{keywords or "指定なし"}
【その他の要望】{notes or "なし"}

SEOに関する指示：
- 記事タイトルは32文字前後とし、キーワードをできるだけ先頭寄りに含める
- メタディスクリプションを120〜160字で別途作成する（検索結果に表示される要約文）
- 各H2見出しにキーワードまたはその類義語を自然に含める
- リード文（導入）の冒頭150字程度で、読者の検索意図（何を知りたくて来たか）に応える
- キーワードは不自然に連呼せず、文章全体で自然な頻度になるようにする
- まとめの最後に、読者の次の行動を促す一文（CTA）を入れる

出力フォーマット：
- 記事タイトル
- メタディスクリプション
- リード文（導入）
- 見出し付きの本文（H2・H3を適切に使用）
- まとめ（CTA付き）

マークダウン形式で出力してください。"""

        with st.spinner("記事を生成中..."):
            try:
                result = generate(prompt)
                st.success("生成完了！")
                st.markdown("---")
                st.markdown(result)
                st.download_button(
                    "📥 テキストとしてダウンロード",
                    data=result,
                    file_name="blog_article.md",
                    mime="text/markdown",
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
