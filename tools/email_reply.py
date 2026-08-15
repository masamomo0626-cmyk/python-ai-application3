import streamlit as st
from utils.gemini import generate

def render():
    st.header("📧 メール返信文作成")
    st.caption("受け取ったメールと返信の意図を入力すると、適切な返信文を生成します。")

    received_email = st.text_area("受け取ったメール本文", placeholder="ここに返信したいメールの内容を貼り付けてください...", height=180)

    col1, col2 = st.columns(2)
    with col1:
        intent = st.text_area("返信の意図・伝えたいこと", placeholder="例：会議の日程を了承する、質問に回答する、丁重に断る", height=100)
        relation = st.selectbox("相手との関係", ["上司・取引先（敬語）", "同僚（丁寧語）", "友人・知人（カジュアル）"])
    with col2:
        reply_length = st.selectbox("返信の長さ", ["簡潔（3〜5行）", "普通（5〜10行）", "詳細（10行以上）"])
        language = st.selectbox("返信言語", ["日本語", "英語"])

    notes = st.text_input("その他の注意事項", placeholder="例：添付ファイルについて触れる、次回の連絡日を入れる")

    if st.button("返信文を生成する", type="primary", use_container_width=True):
        if not received_email or not intent:
            st.warning("受け取ったメールと返信の意図を入力してください。")
            return

        prompt = f"""以下の条件でメールの返信文を作成してください。

【受け取ったメール】
{received_email}

【返信の意図・伝えたいこと】
{intent}

【相手との関係】{relation}
【返信の長さ】{reply_length}
【返信言語】{language}
【その他の注意事項】{notes or "なし"}

宛名・署名欄は「〇〇様」「敬具」などプレースホルダーで示してください。
返信文のみを出力し、説明文は不要です。"""

        with st.spinner("返信文を生成中..."):
            try:
                result = generate(prompt)
                st.success("生成完了！")
                st.markdown("---")
                st.text_area("生成された返信文", value=result, height=300)
                st.download_button(
                    "📥 テキストとしてダウンロード",
                    data=result,
                    file_name="email_reply.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
