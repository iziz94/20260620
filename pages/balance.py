import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="커리어 성향 게임", page_icon="🎮")

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
# 질문 (가중치 + 게임형)
# =========================
questions = [
    {"q":"새 프로젝트를 맡았을 때", "w":2.0,
     "a":("혼자 구조를 설계한다","solo"),
     "b":("팀과 계속 협업한다","team")},

    {"q":"문제를 해결할 때", "w":1.8,
     "a":("논리적으로 분석한다","logic"),
     "b":("직관과 아이디어로 해결한다","creative")},

    {"q":"일 선택 기준", "w":1.6,
     "a":("안정적인 환경","stability"),
     "b":("성장 가능한 도전","challenge")},

    {"q":"업무 스타일", "w":1.3,
     "a":("자유롭게 일한다","freedom"),
     "b":("규칙과 구조 선호","stability")},

    {"q":"성과 기준", "w":1.4,
     "a":("빠른 결과","speed"),
     "b":("완성도 높은 결과","logic")},

    {"q":"사람들과 일할 때", "w":1.5,
     "a":("도와주는 역할","help"),
     "b":("협업 구조 만들기","team")},

    {"q":"아이디어 처리 방식", "w":1.2,
     "a":("창의적으로 확장","creative"),
     "b":("현실적으로 정리","logic")},

    {"q":"스트레스 상황", "w":1.0,
     "a":("혼자 해결","solo"),
     "b":("함께 해결","team")},

    {"q":"새로운 기술 학습", "w":1.3,
     "a":("혼자 깊게 탐구","solo"),
     "b":("사람들과 같이 학습","team")},

    {"q":"회의 스타일", "w":1.2,
     "a":("빠르게 결정","speed"),
     "b":("충분한 토론","team")},

    {"q":"문제 발생 시", "w":1.4,
     "a":("원인 분석","logic"),
     "b":("새로운 시도","creative")},

    {"q":"업무 만족 기준", "w":1.3,
     "a":("자유도","freedom"),
     "b":("안정성","stability")},
]

# =========================
# 직업 데이터
# =========================
job_profiles = {
    "소프트웨어 엔지니어": {
        "traits": ["logic","solo"],
        "salary": "5000~12000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "시스템과 서비스를 개발하는 직업"
    },
    "데이터 사이언티스트": {
        "traits": ["logic","solo"],
        "salary": "6000~13000만원",
        "difficulty": "⭐⭐⭐⭐⭐",
        "desc": "데이터 분석 전문가"
    },
    "UX/UI 디자이너": {
        "traits": ["creative"],
        "salary": "4000~9000만원",
        "difficulty": "⭐⭐⭐☆☆",
        "desc": "사용자 경험 디자인"
    },
    "프로덕트 매니저": {
        "traits": ["team","logic"],
        "salary": "6000~15000만원",
        "difficulty": "⭐⭐⭐⭐☆",
        "desc": "제품 전략 및 팀 조율"
    },
    "마케터": {
        "traits": ["creative","team","fun"],
        "salary": "3500~10000만원",
        "difficulty": "⭐⭐⭐☆☆",
        "desc": "브랜드 전략 전문가"
    },
    "창업가": {
        "traits": ["challenge","freedom","speed"],
        "salary": "변동",
        "difficulty": "⭐⭐⭐⭐⭐",
        "desc": "사업을 만드는 사람"
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
    for m, ts in mbti_map.items():
        s = sum(score.get(t,0) for t in ts)
        if s > best_score:
            best, best_score = m, s
    return best or "INFP"

# =========================
# AI 성향 설명
# =========================
def explain_personality(score):
    sorted_traits = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top = [t[0] for t in sorted_traits[:3]]

    mapping = {
        "solo":"👉 혼자 집중하며 깊게 사고하는 성향",
        "team":"👉 사람들과 협업하며 시너지를 내는 성향",
        "logic":"👉 논리적이고 구조적으로 사고하는 성향",
        "creative":"👉 창의적이고 아이디어 중심적인 성향",
        "freedom":"👉 자유로운 환경에서 능력을 발휘하는 성향",
        "stability":"👉 안정적이고 계획적인 환경 선호",
        "challenge":"👉 도전을 통해 성장하는 성향",
        "speed":"👉 빠른 판단과 실행력",
        "help":"👉 타인을 돕는 것에서 만족",
        "fun":"👉 재미와 흥미 중심"
    }

    text = "🧠 핵심 성향 분석\n\n"
    for t in top:
        text += mapping.get(t,"") + "\n\n"
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
# 캐릭터 이미지
# =========================
character_img = "https://images.unsplash.com/photo-1607746882042-944635dfe10e"

# =========================
# UI 시작
# =========================
st.title("🎮 커리어 성향 게임")

# =========================
# 질문 진행
# =========================
if st.session_state.i < len(questions):

    q = questions[st.session_state.i]

    st.write(f"Q{st.session_state.i+1}/{len(questions)}")
    st.progress(st.session_state.i / len(questions))

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

    st.success("🎯 분석 완료")

    # 성향 분석
    st.subheader("🧠 성향 분석")
    draw_radar(st.session_state.score)

    st.subheader("🤖 AI 성향 설명")
    st.write(explain_personality(st.session_state.score))

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

        st.write("🧠", info["desc"])
        st.write("💰 연봉:", info["salary"])
        st.write("📊 난이도:", info["difficulty"])
        st.write("🔗 성향:", info["traits"])

        if st.button("⬅ 뒤로"):
            st.session_state.selected_job = None
            st.rerun()

    # =========================
    # 엔딩 캐릭터
    # =========================
    st.markdown("---")
    st.subheader("🎁 당신의 커리어 가이드")

    st.image(character_img, use_container_width=True)

    st.write("""
    당신의 선택을 기반으로 분석한 결과입니다.  
    이 결과는 정답이 아니라 당신의 가능성을 보여주는 지도입니다.
    """)

    # =========================
    # 재시작
    # =========================
    if st.button("🔄 다시 시작"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.session_state.selected_job = None
        st.rerun()
