import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="커리어 성향 테스트", page_icon="💼")

# =========================
# CSS
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
# 질문
# =========================
questions = [
    ("혼자 vs 팀", ("혼자 공부","solo"), ("팀 공부","team")),
    ("창의 vs 논리", ("창의","creative"), ("논리","logic")),
    ("안정 vs 도전", ("안정","stability"), ("도전","challenge")),
    ("자유 vs 규칙", ("자유","freedom"), ("규칙","stability")),
    ("재미 vs 효율", ("재미","fun"), ("효율","logic")),
    ("도움 vs 분석", ("도움","help"), ("분석","logic")),
    ("빠름 vs 정확", ("빠름","speed"), ("정확","logic")),
    ("혼자 작업 vs 협업", ("혼자","solo"), ("협업","team")),
]

# =========================
# 직업 데이터
# =========================
job_profiles = {
    "소프트웨어 엔지니어": {
        "traits": ["logic", "solo"],
        "salary": "5000~12000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "논리 기반으로 시스템과 서비스를 개발하는 직업입니다."
    },
    "데이터 사이언티스트": {
        "traits": ["logic", "solo"],
        "salary": "6000~13000만원",
        "difficulty": "⭐⭐⭐⭐⭐",
        "desc": "데이터를 분석해 의사결정을 돕는 직업입니다."
    },
    "UX/UI 디자이너": {
        "traits": ["creative"],
        "salary": "4000~9000만원",
        "difficulty": "⭐⭐⭐☆☆",
        "desc": "사용자 경험을 설계하는 디자인 직업입니다."
    },
    "프로덕트 매니저": {
        "traits": ["team", "logic"],
        "salary": "6000~15000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "제품 방향과 팀을 조율하는 핵심 역할입니다."
    },
    "마케터": {
        "traits": ["creative", "team", "fun"],
        "salary": "3500~10000만원",
        "difficulty": "⭐⭐⭐☆☆",
        "desc": "브랜드와 제품을 시장에 알리는 직업입니다."
    },
    "창업가": {
        "traits": ["challenge", "freedom", "speed"],
        "salary": "변동 매우 큼",
        "difficulty": "⭐⭐⭐⭐⭐",
        "desc": "새로운 사업을 만들어 성장시키는 직업입니다."
    },
    "교사": {
        "traits": ["help", "stability", "team"],
        "salary": "3000~6000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "학생을 교육하고 성장시키는 직업입니다."
    },
    "상담사": {
        "traits": ["help", "team"],
        "salary": "3000~7000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "사람들의 심리와 문제를 돕는 직업입니다."
    },
}

# =========================
# 상태 초기화
# =========================
if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}

if "selected_job" not in st.session_state:
    st.session_state.selected_job = None

# =========================
# MBTI (재미용)
# =========================
mbti_map = {
    "INTJ":["logic","solo"],
    "ENTP":["creative","challenge"],
    "INFP":["creative","freedom"],
    "ESTJ":["stability","team"]
}

def get_mbti(score):
    best, best_score = None, 0
    for mbti, ts in mbti_map.items():
        s = sum(score.get(t,0) for t in ts)
        if s > best_score:
            best, best_score = mbti, s
    return best or "INFP"

# =========================
# 레이더 차트
# =========================
def draw_radar(score):
    values = [score.get(t, 0) for t in traits]
    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(traits), endpoint=False).tolist()
    angles += angles[:1]

    fig = plt.figure()
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2)
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
        match = sum(score.get(t, 0) for t in info["traits"])
        results.append((job, match))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]

# =========================
# 질문 화면
# =========================
st.title("💼 성향 기반 커리어 테스트")

if st.session_state.i < len(questions):

    q = questions[st.session_state.i]

    st.subheader(q[0])

    col1, col2 = st.columns(2)

    if col1.button(q[1][0]):
        st.session_state.score[q[1][1]] = st.session_state.score.get(q[1][1],0)+1
        st.session_state.i += 1
        st.rerun()

    if col2.button(q[2][0]):
        st.session_state.score[q[2][1]] = st.session_state.score.get(q[2][1],0)+1
        st.session_state.i += 1
        st.rerun()

# =========================
# 결과 화면
# =========================
else:

    st.success("결과 분석 완료")

    st.subheader("🧠 성향 분석")
    draw_radar(st.session_state.score)

    mbti = get_mbti(st.session_state.score)
    st.write(f"🎭 재미 MBTI: {mbti}")

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

        st.write(f"🧠 설명: {info['desc']}")
        st.write(f"💰 연봉: {info['salary']}")
        st.write(f"📊 난이도: {info['difficulty']}")
        st.write(f"🔗 성향: {', '.join(info['traits'])}")

        if st.button("⬅ 뒤로가기"):
            st.session_state.selected_job = None
            st.rerun()

    # 다시 시작
    if st.button("🔄 다시 시작"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.session_state.selected_job = None
        st.rerun()
