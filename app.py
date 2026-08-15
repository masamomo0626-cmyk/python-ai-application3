import os
import streamlit as st
from tools import blog_writer, email_reply, summarizer, proofreader, sns_writer, catchphrase, translator

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

TOOLS = {
    "📝 ブログ記事執筆": blog_writer.render,
    "📧 メール返信文作成": email_reply.render,
    "📋 文章要約": summarizer.render,
    "✏️ 文章校正・リライト": proofreader.render,
    "📱 SNS投稿文作成": sns_writer.render,
    "💡 キャッチコピー・タイトル生成": catchphrase.render,
    "🌐 翻訳": translator.render,
}

with st.sidebar:
    st.title("✍️ AI ライティングツール")
    st.caption("Powered by Google Gemini")
    st.markdown("---")
    st.markdown("**ツールを選択してください**")

    selected = st.radio(
        "ツール選択",
        list(TOOLS.keys()),
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**モデル設定**")

    selected_model = st.selectbox(
        "使用モデル",
        [
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
        ],
        help="gemini-2.5-flash-lite が動作確認済みで最も軽量です。",
    )
    os.environ["GEMINI_MODEL"] = selected_model

    st.markdown("---")
    st.markdown("**API キー設定**")

    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder=".env に設定済みの場合は不要",
        help=".env ファイルに GEMINI_API_KEY を設定するか、ここに直接入力してください。",
    )
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.success("API キーを設定しました")

    st.markdown("---")
    st.caption("© 2026 AI Writing Tool")

TOOLS[selected]()
