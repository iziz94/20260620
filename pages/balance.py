import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="커리어 스토리 게임", page_icon="🎮")

# =========================
# 스타일
# =========================
st.markdown("""
<style>
.stButton button {
    width: 100%;
    height: 60px;
    font-size: 16px;
    border-radius: 12px;
    transition: 0.2s;
}

.stButton button:hover {
    transform: scale(1.05);
    background-color: #4f46e5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 성향 리스트
# =========================
traits = [
    "solo","team","creative","logic","help",
    "freedom","stability","fun","challenge","speed"
]

# =========================
# 🎮 스토리형 질문
# =========================
questions = [
    {"level":1, "story":"📚 새로운 학교에 첫 등교한 날", "q":"너는 어떻게 할까?",
     "w":2.0,
     "a":("혼자 조용히 자리 잡는다","solo"),
     "b":("친구들에게 먼저 다가간다","team")},

    {"level":2, "story":"🧩 어려운 숙제가 나왔다", "q":"너의 선택은?",
     "w":1.8,
     "a":("끝까지 혼자 해결한다","logic"),
     "b":("새로운 방법을 떠올린다","creative")},

    {"level":3, "story":"🎮 새로운 게임을 시작했다", "q":"너는?",
     "w":1.6,
     "a":("규칙부터 꼼꼼히 본다","stability"),
     "b":("일단 하면서 배운다","challenge")},

    {"level":4, "story":"🏫 조별 과제가 생겼다", "q":"너는?",
     "w":1.5,
     "a":("역할 나눠서 한다","team"),
     "b":("내가 중심이 되어 한다","solo")},

    {"level":5, "story":"⚡ 문제가 갑자기 생겼다", "q":"너는?",
     "w":1.4,
     "a":("원인을 분석한다","logic"),
     "b":("새 방법을 떠올린다","creative")},

    {"level":6, "story":"⏰ 시간이 부족한 상황", "q":"너는?",
     "w":1.3,
     "a":("빠르게 끝낸다","speed"),
     "b":("천천히 정확하게 한다","logic")},

    {"level":7, "story":"🎨 자유 시간이 생겼다", "q":"너는?",
     "w":1.2,
     "a":("혼자 쉰다","solo"),
     "b":("친구들과 논다","team")},

    {"level":8, "story":"🚀 마지막 미션", "q":"너의 선택은?",
     "w":2.0,
     "a":("안정적인 길","stability"),
     "b":("도전적인 길","challenge")},
]

# =========================
# 직업 데이터
# =========================
job_profiles = {
    "소프트웨어 엔지니어": {
        "traits": ["logic","solo"],
        "salary": "5000~12000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "앱과 시스템을 만드는 직업"
    },
    "데이터 분석가": {
        "traits": ["logic","solo"],
        "salary": "6000~13000만원",
        "difficulty": "⭐⭐⭐⭐⭐",
        "desc": "데이터를 분석해서 의미를 찾는 직업"
    },
    "UX 디자이너": {
        "traits": ["creative"],
        "salary": "4000~9000만원",
        "difficulty": "⭐⭐⭐☆☆",
        "desc": "사용자 경험을 디자인하는 직업"
    },
    "마케터": {
        "traits": ["creative","team"],
        "salary": "3500~10000만원",
        "difficulty": "⭐⭐⭐☆☆",
        "desc": "사람들에게 제품을 알리는 직업"
    },
    "기획자": {
        "traits": ["team","logic"],
        "salary": "5000~14000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "서비스를 설계하고 팀을 이끄는 직업"
    },
}

# =========================
# 상태 초기화
# =========================
if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}
    st.session_state.selected_job = None

# =========================
# AI 쉬운 설명
# =========================
def explain_personality(score):

    sorted_traits = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top = [t[0] for t in sorted_traits[:3]]

    easy_map = {
        "solo":"🧍 혼자 있을 때 집중을 잘하고 혼자 하는 일을 좋아해!",
        "team":"👥 친구들이랑 같이 있을 때 더 힘이 나는 스타일이야!",
        "logic":"🧠 생각을 차근차근 정리하는 걸 좋아해!",
        "creative":"💡 새로운 아이디어를 잘 떠올리는 편이야!",
        "freedom":"🌿 자유로운 환경을 좋아해!",
        "stability":"📋 안정적인 걸 좋아해!",
        "challenge":"🔥 어려운 일을 도전처럼 즐겨!",
        "speed":"⚡ 빠르게 결정하고 행동하는 스타일!",
        "help":"🤝 다른 사람 도와주는 걸 좋아해!",
        "fun":"🎉 재미있는 게 가장 중요해!"
    }

    text = "🧠 너의 성향을 쉽게 설명해줄게!\n\n"

    for t in top:
        text += easy_map.get(t,"") + "\n\n"

    text += "✨ 이건 정답이 아니라 너의 성향이야!"

    return text

# =========================
# 레이더 차트
# =========================
def draw_radar(score):
    values = [score.get(t,0) for t in traits]
    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(traits), endpoint=False).tolist()
    angles += angles[:1]

    fig = plt.figure()
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(traits)

    st.pyplot(fig)

# =========================
# 직업 추천
# =========================
def recommend_jobs(score):
    results = []

    for job, info in job_profiles.items():
        match = sum(score.get(t,0) for t in info["traits"])
        results.append((job, match))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]

# =========================
# UI 시작
# =========================
st.title("🎮 커리어 스토리 게임")

# =========================
# 질문 진행
# =========================
if st.session_state.i < len(questions):

    q = questions[st.session_state.i]

    st.write(f"🎮 LEVEL {q['level']}")
    st.progress((st.session_state.i + 1) / len(questions))

    st.markdown(f"### {q['story']}")
    st.subheader(q["q"])

    col1, col2 = st.columns(2)

    if col1.button(q["a"][0]):
        st.session_state.score[q["a"][1]] = st.session_state.score.get(q["a"][1],0) + q["w"]
        st.session_state.i += 1
        st.rerun()

    if col2.button(q["b"][0]):
        st.session_state.score[q["b"][1]] = st.session_state.score.get(q["b"][1],0) + q["w"]
        st.session_state.i += 1
        st.rerun()

# =========================
# 결과 화면
# =========================
else:

    st.success("🎯 분석 완료!")

    # 레이더 차트
    st.subheader("📊 너의 성향 그래프")
    draw_radar(st.session_state.score)

    # AI 설명
    st.subheader("🤖 AI 쉬운 설명")
    st.write(explain_personality(st.session_state.score))

    # 직업 추천
    st.subheader("💼 추천 직업 TOP 5")

    top_jobs = recommend_jobs(st.session_state.score)

    for job, score in top_jobs:
        if st.button(f"{job} ({score}점)"):
            st.session_state.selected_job = job

    # =========================
    # 직업 상세 페이지
    # =========================
    if st.session_state.selected_job:

        job = st.session_state.selected_job
        info = job_profiles[job]

        st.markdown("---")
        st.subheader(f"📌 {job}")

        st.write("🧠 설명:", info["desc"])
        st.write("💰 연봉:", info["salary"])
        st.write("📊 난이도:", info["difficulty"])
        st.write("🔗 성향:", info["traits"])

        if st.button("⬅ 뒤로"):
            st.session_state.selected_job = None
            st.rerun()

    # =========================
    # 다시 시작
    # =========================
    st.markdown("---")

    if st.button("🔄 다시 시작"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.session_state.selected_job = None
        st.rerun()
