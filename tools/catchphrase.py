import streamlit as st
from utils.gemini import generate

def render():
    st.header("💡 キャッチコピー・タイトル生成")
    st.caption("商品・サービス・コンテンツの特徴を入力すると、魅力的なコピーやタイトルを生成します。")

    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("対象（商品・サービス・記事など）", placeholder="例：オーガニックコーヒー、ダイエットアプリ、ブログ記事")
        target = st.text_input("ターゲット", placeholder="例：健康意識の高い30代女性")
    with col2:
        genre = st.selectbox("コピーの種類", [
            "キャッチコピー（広告・マーケティング向け）",
            "ブログ・記事タイトル（SEO向け）",
            "商品紹介文の見出し",
            "メールの件名",
            "プレゼンのタイトル",
        ])
        count = st.slider("生成する数", min_value=3, max_value=10, value=5)

    features = st.text_area("特徴・強み・伝えたいこと", placeholder="例：無農薬、深煎り、ブラジル産、リッチな味わい、毎朝の贅沢", height=80)
    keywords = st.text_input("含めたいキーワード（カンマ区切り）", placeholder="例：本格、こだわり、毎日")
    vibe = st.selectbox("雰囲気・イメージ", [
        "高級感・上質",
        "元気・エネルギッシュ",
        "癒し・ほっこり",
        "信頼・安心",
        "挑戦・革新",
        "おしゃれ・スタイリッシュ",
    ])

    if st.button("コピーを生成する", type="primary", use_container_width=True):
        if not subject or not features:
            st.warning("対象と特徴を入力してください。")
            return

        prompt = f"""以下の条件で{genre}を{count}個作成してください。

【対象】{subject}
【ターゲット】{target or "一般的なユーザー"}
【種類】{genre}
【特徴・強み・伝えたいこと】{features}
【含めたいキーワード】{keywords or "なし"}
【雰囲気・イメージ】{vibe}

各コピーは番号付きで1行ずつ出力してください。
説明文や前置きは不要です。コピーのみ出力してください。"""

        with st.spinner("コピーを生成中..."):
            try:
                result = generate(prompt)
                st.success("生成完了！")
                st.markdown("---")
                st.markdown(f"### 生成された{genre}")

                lines = [line.strip() for line in result.strip().split("\n") if line.strip()]
                for line in lines:
                    st.markdown(f"- {line}")

                st.download_button(
                    "📥 テキストとしてダウンロード",
                    data=result,
                    file_name="catchphrases.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
