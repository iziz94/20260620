import streamlit as st
import matplotlib.pyplot as plt
import time

# =========================
# 페이지 설정 (최상단 필수)
# =========================
st.set_page_config(page_title="MBTI 고양이 테스트", page_icon="🐱")

# =========================
# CSS
# =========================
st.markdown("""
<style>
img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: 12px;
    transition: 0.3s;
}

img:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# MBTI → 고양이 이미지
# =========================
mbti_cat = {
    "INTJ":"https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "INTP":"https://images.unsplash.com/photo-1533738363-b7f9aef128ce",
    "ENTJ":"https://images.unsplash.com/photo-1543852786-1cf6624b9987",
    "ENTP":"https://images.unsplash.com/photo-1543852786-1cf6624b9987",
    "INFJ":"https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "INFP":"https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "ENFP":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    "ESFP":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
}

# =========================
# MBTI 로직
# =========================
mbti_map = {
    "INTJ":["logic","solo","stability"],
    "INTP":["logic","solo","creative"],
    "ENTJ":["challenge","logic","team"],
    "ENTP":["creative","challenge","fun"],
    "INFJ":["help","solo","stability"],
    "INFP":["creative","solo","freedom"],
    "ENFP":["creative","freedom","fun"],
    "ESFP":["fun","team","freedom"],
    "ISTJ":["stability","logic","solo"],
    "ISFJ":["help","stability","team"],
    "ESTJ":["stability","team","logic"],
    "ESFJ":["team","help","fun"],
    "ISTP":["logic","solo","challenge"],
    "ISFP":["creative","solo","freedom"],
    "ESTP":["speed","challenge","fun"],
}

# =========================
# 질문
# =========================
questions = [
    {
        "q":"혼자 vs 팀",
        "a":{"text":"혼자 공부","tag":"solo","img":"https://source.unsplash.com/800x600/?studying,alone"},
        "b":{"text":"팀 공부","tag":"team","img":"https://source.unsplash.com/800x600/?team,meeting"}
    },
    {
        "q":"안정 vs 도전",
        "a":{"text":"안정","tag":"stability","img":"https://source.unsplash.com/800x600/?calm,office"},
        "b":{"text":"도전","tag":"challenge","img":"https://source.unsplash.com/800x600/?mountain,climb"}
    },
    {
        "q":"창작 vs 논리",
        "a":{"text":"창작","tag":"creative","img":"https://source.unsplash.com/800x600/?art,creative"},
        "b":{"text":"논리","tag":"logic","img":"https://source.unsplash.com/800x600/?coding,computer"}
    },
    {
        "q":"자유 vs 규칙",
        "a":{"text":"자유","tag":"freedom","img":"https://source.unsplash.com/800x600/?travel,freedom"},
        "b":{"text":"규칙","tag":"stability","img":"https://source.unsplash.com/800x600/?planning,notes"}
    },
]

# =========================
# MBTI 계산
# =========================
def get_mbti(score):
    best, best_score = None, 0
    for mbti, traits in mbti_map.items():
        s = sum(score.get(t,0) for t in traits)
        if s > best_score:
            best, best_score = mbti, s
    return best or "INFP"

# =========================
# 그래프
# =========================
def draw_chart(score):
    fig, ax = plt.subplots()
    ax.bar(score.keys(), score.values(), color="#4f46e5")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =========================
# 상태 초기화
# =========================
if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}
    st.session_state.last = None

st.title("🐱 MBTI 고양이 테스트")

# =========================
# 질문 화면
# =========================
if st.session_state.i < len(questions):

    q = questions[st.session_state.i]
    st.subheader(q["q"])

    col1, col2 = st.columns(2)

    with col1:
        st.image(q["a"]["img"])
        if st.button(q["a"]["text"]):
            st.session_state.score[q["a"]["tag"]] = st.session_state.score.get(q["a"]["tag"],0)+1
            st.session_state.last = q["a"]["tag"]
            st.session_state.i += 1
            st.rerun()

    with col2:
        st.image(q["b"]["img"])
        if st.button(q["b"]["text"]):
            st.session_state.score[q["b"]["tag"]] = st.session_state.score.get(q["b"]["tag"],0)+1
            st.session_state.last = q["b"]["tag"]
            st.session_state.i += 1
            st.rerun()

# =========================
# 결과
# =========================
else:

    st.success("결과 분석 중...")

    progress = st.progress(0)
    for i in range(60):
        time.sleep(0.01)
        progress.progress(i+1)

    mbti = get_mbti(st.session_state.score)

    st.subheader(f"🧠 당신의 MBTI: {mbti}")

    draw_chart(st.session_state.score)

    st.subheader("🐱 당신의 고양이")
    if mbti in mbti_cat:
        st.image(mbti_cat[mbti])

    if st.button("🔄 다시 시작"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.session_state.last = None
        st.rerun()
