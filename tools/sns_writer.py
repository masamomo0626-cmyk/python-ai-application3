import streamlit as st
from utils.gemini import generate

PLATFORM_SPECS = {
    "Twitter / X": {"chars": "140文字以内", "style": "簡潔でインパクトのある、ハッシュタグ付き"},
    "Instagram": {"chars": "2200文字以内", "style": "絵文字を適度に使い、ハッシュタグを末尾にまとめる"},
    "Facebook": {"chars": "500字程度", "style": "親しみやすく、シェアされやすい"},
    "LinkedIn": {"chars": "700字程度", "style": "プロフェッショナルで知識・経験を伝える"},
    "Threads": {"chars": "500文字以内", "style": "カジュアルで会話的"},
}

def render():
    st.header("📱 SNS投稿文作成")
    st.caption("投稿内容のテーマや要点を入力すると、各SNSに最適化した投稿文を生成します。")

    topic = st.text_area("投稿したい内容・テーマ・伝えたいこと", placeholder="例：新しいカフェをオープンしました。こだわりのコーヒーと落ち着いた空間が魅力です。", height=120)

    col1, col2 = st.columns(2)
    with col1:
        platforms = st.multiselect(
            "投稿するSNSを選択（複数可）",
            list(PLATFORM_SPECS.keys()),
            default=["Twitter / X"],
        )
        count = st.slider("バリエーション数", min_value=1, max_value=3, value=2)
    with col2:
        purpose = st.selectbox("投稿の目的", ["認知拡大・宣伝", "エンゲージメント向上（いいね・シェア）", "情報提供・教育", "日常・雑談"])
        tone = st.selectbox("投稿のトーン", ["フレンドリー・親しみやすい", "プロフェッショナル", "ユーモラス・面白い", "感動・共感を呼ぶ"])

    if st.button("投稿文を生成する", type="primary", use_container_width=True):
        if not topic:
            st.warning("投稿内容を入力してください。")
            return
        if not platforms:
            st.warning("SNSプラットフォームを1つ以上選択してください。")
            return

        with st.spinner("投稿文を生成中..."):
            for platform in platforms:
                spec = PLATFORM_SPECS[platform]
                prompt = f"""以下の条件でSNS投稿文を{count}パターン作成してください。

【プラットフォーム】{platform}
【文字数制限】{spec["chars"]}
【推奨スタイル】{spec["style"]}
【投稿の内容・テーマ】{topic}
【投稿の目的】{purpose}
【トーン】{tone}

各パターンは「パターン1」「パターン2」のように番号で区切って出力してください。
説明文は不要です。投稿文のみ出力してください。"""

                try:
                    result = generate(prompt)
                    st.markdown(f"### {platform}")
                    st.text_area(f"{platform} 投稿文", value=result, height=200, key=platform)
                    st.download_button(
                        f"📥 {platform} の投稿文をダウンロード",
                        data=result,
                        file_name=f"sns_{platform.replace(' / ', '_').lower()}.txt",
                        mime="text/plain",
                        key=f"dl_{platform}",
                    )
                    st.markdown("---")
                except Exception as e:
                    st.error(f"{platform}: エラーが発生しました: {e}")
