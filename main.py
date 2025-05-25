# 🌟 PLAVE 追星生活助理｜整合版
# pip install streamlit pandas requests

import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="PLAVE 追星助理", page_icon="🎀", layout="centered")
page = st.sidebar.radio("選擇功能", ["📅 行程倒數助手", "🎤 成員小百科", "💱 匯率助手"])

if page == "📅 行程倒數助手":
    st.title("📅 PLAVE 行程倒數助手｜分類＋倒數")
    category_options = ["官方活動", "粉絲應援", "演唱會資訊", "節目出演", "社群直播", "其他"]

    if "schedule" not in st.session_state:
        st.session_state.schedule = [
            {"活動名稱": "PLAVE LIVE IN SEOUL", "時間": "2025-06-08 18:00", "類別": "演唱會資訊"},
            {"活動名稱": "官方 IG LIVE", "時間": "2025-06-03 21:00", "類別": "官方活動"},
            {"活動名稱": "生日杯套活動開跑", "時間": "2025-06-05 10:00", "類別": "粉絲應援"},
        ]

    st.markdown("### ➕ 新增行程")
    with st.form("add_form"):
        new_name = st.text_input("活動名稱")
        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("活動日期", value=datetime.now().date())
        with col2:
            time_input = st.time_input("活動時間", value=datetime.now().time())
        new_cat = st.selectbox("活動類別", category_options)
        submitted = st.form_submit_button("新增")
        if submitted and new_name:
            new_time = datetime.combine(date_input, time_input)
            st.session_state.schedule.append({
                "活動名稱": new_name,
                "時間": new_time.strftime("%Y-%m-%d %H:%M"),
                "類別": new_cat
            })
            st.success("✅ 已新增活動")

    df_display = pd.DataFrame(st.session_state.schedule)
    df_display["時間"] = pd.to_datetime(df_display["時間"])
    st.markdown("### 📋 行程表")
    st.dataframe(df_display.sort_values("時間"), use_container_width=True)

    st.markdown("### ⏰ 倒數提醒")
    if len(df_display) > 0:
        selected = st.selectbox("選擇活動", df_display["活動名稱"].tolist())
        selected_row = df_display[df_display["活動名稱"] == selected].iloc[0]
        target_time = pd.to_datetime(selected_row["時間"])
        category = selected_row["類別"]
        now = datetime.now()
        delta = target_time - now
        if delta.total_seconds() > 0:
            st.success(f"🗂 類別：{category}")
            st.success(f"距離「{selected}」活動還有：{delta.days} 天 {delta.seconds//3600} 小時 {(delta.seconds%3600)//60} 分鐘")
        else:
            st.warning(f"「{selected}」活動已經開始或結束！")
    else:
        st.info("尚無行程，請新增。")

elif page == "🎤 成員小百科":
    st.title("🎤 PLAVE 成員小百科")
    members = {
        "Yejun / 藝俊": {"生日": "2001.09.12", "年齡": "22", "身高": "183 cm", "血型": "B",
                         "擔當": "隊長、Vocal", "符號": "🐬💙", "MBTI": "ISFJ-T",
                         "興趣": "彈吉他、跑步、喝咖啡", "特長": "作詞作曲、跑步？",
                         "喜歡": "音樂、咖啡、辣的食物、可愛動物", "討厭": "蟲子、炎熱的天氣"},
        "Noah / 諾亞": {"生日": "2001.02.10", "年齡": "22", "身高": "179 cm", "血型": "O",
                        "擔當": "自稱舞蹈（實際：Vocal）", "符號": "🦙💜", "MBTI": "ISTJ-A",
                        "興趣": "唱歌、重訓、看電影", "特長": "作詞作曲、跳高？",
                        "喜歡": "音樂、健身、咖啡", "討厭": "蟲子、嘈雜的地方、無禮的人、昏沈感"},
        "Bamby / 斑比": {"生日": "2002.07.15", "年齡": "21", "身高": "174 cm", "血型": "B",
                         "擔當": "舞蹈、Vocal", "符號": "🦌💗", "MBTI": "INFP-T",
                         "興趣": "跳舞、運動、演戲、看 Netflix", "特長": "跳舞、演戲、運動",
                         "喜歡": "平壤冷麵、小狗、散步", "討厭": "又高又帥的人（銀虎）"},
        "Eunho / 銀虎": {"生日": "2003.05.24", "年齡": "20", "身高": "184 cm", "血型": "A",
                         "擔當": "RAP、Vocal", "符號": "🐺❤️", "MBTI": "ENTP-T",
                         "興趣": "重訓、游泳、看電影", "特長": "作曲、寫歌詞、RAP、游泳",
                         "喜歡": "音樂、重訓、查餐廳跟……你們？", "討厭": "沒禮貌的人、虛偽、太吵"},
        "Hamin / 河玟": {"生日": "11月1日", "年齡": "20", "身高": "185 cm", "血型": "AB",
                         "擔當": "RAP、舞蹈", "符號": "🐈‍⬛ 🖤", "MBTI": "ISFJ-T",
                         "興趣": "畫畫、保齡球、看影片、足球", "特長": "RAP、舞蹈、跆拳道",
                         "喜歡": "食物、鍛鍊、讚美、遊戲", "討厭": "謊言、蚊子"}
    }
    selected = st.selectbox("請選擇一位成員", list(members.keys()))
    info = members[selected]
    st.markdown(f"### {selected}")
    for k, v in info.items():
        st.markdown(f"**{k}**：{v}")

elif page == "💱 匯率助手":
    st.title("💱 偶像周邊匯率比較小幫手")
    jpy = st.number_input("💴 日圓價格", min_value=0.0, format="%.2f")
    usd = st.number_input("💵 美元價格", min_value=0.0, format="%.2f")
    krw = st.number_input("🇰🇷 韓圓價格", min_value=0.0, format="%.2f")

    @st.cache_data
    def get_rates():
        res = requests.get("https://open.er-api.com/v6/latest/USD")
        return res.json()["rates"]

    rates = get_rates()

    def convert(amount, cur):
        rate = rates["TWD"] / rates[cur]
        return round(rate, 3), round(amount * rate, 2)

    results = []
    for cur, amt in [("JPY", jpy), ("USD", usd), ("KRW", krw)]:
        rate, twd = convert(amt, cur)
        results.append((cur, amt, rate, twd))

    st.markdown("## 💖 換算結果")
    if any(r[1] > 0 for r in results):
        min_cost = min(r[3] for r in results if r[3] > 0)
        for cur, amt, rate, twd in results:
            if amt == 0:
                continue
            tag = "🌟 最划算！" if twd == min_cost else ""
            st.markdown(f"使用 **{cur}** 付款：{amt} → 約 **{twd} TWD**（1 {cur} ≈ {rate}）{tag}")
    else:
        st.info("請輸入任一金額來換算")

st.caption("📦 PLAVE AI 助理｜整合版 by ChatGPT")
