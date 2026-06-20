import streamlit as st
import matplotlib.pyplot as plt
import time

# =========================
# 🎨 CSS (이미지 확대 + 버튼 애니메이션)
# =========================
st.markdown("""
<style>
/* 버튼 */
.stButton button {
    width: 100%;
    height: 55px;
    font-size: 16px;
    border-radius: 12px;
    transition: 0.2s;
}

.stButton button:hover {
    transform: scale(1.05);
    background-color: #4f46e5;
    color: white;
}

/* 이미지 hover 확대 */
img {
    border-radius: 12px;
    transition: 0.3s;
}

img:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🧠 MBTI → 고양이
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
# 🧠 MBTI 로직
# =========================
mbti_map = {
    "INTJ":["logic","solo","structure"],
    "INTP":["logic","solo","creative"],
    "ENTJ":["challenge","logic","team"],
    "ENTP":["creative","challenge","fun"],
    "INFJ":["help","solo","structure"],
    "INFP":["creative","solo","freedom"],
    "ENFP":["creative","freedom","fun"],
    "ESFP":["fun","team","freedom"],
    "ISTJ":["stability","structure","logic"],
    "ISFJ":["help","structure","team"],
    "ESTJ":["stability","structure","team"],
    "ESFJ":["team","help","fun"],
    "ISTP":["logic","solo","field"],
    "ISFP":["creative","solo","freedom"],
    "ESTP":["speed","challenge","fun"],
}

# =========================
# 🎮 16문항 밸런스 게임 (이미지 2개 구조)
# =========================
questions = [
    {
        "q":"혼자 집중 vs 팀 협업",
        "a":{"text":"혼자 공부","tag":"solo","img":"https://images.unsplash.com/photo-1521737604893-d14cc237f11d"},
        "b":{"text":"팀 공부","tag":"team","img":"https://images.unsplash.com/photo-1522202176988-66273c2fd55f"}
    },
    {
        "q":"안정 vs 도전",
        "a":{"text":"안정","tag":"stability","img":"https://images.unsplash.com/photo-1521791136064-7986c2920216"},
        "b":{"text":"도전","tag":"challenge","img":"https://images.unsplash.com/photo-1517694712202-14dd9538aa97"}
    },
    {
        "q":"창작 vs 논리",
        "a":{"text":"창작","tag":"creative","img":"https://images.unsplash.com/photo-1513364776144-60967b0f800f"},
        "b":{"text":"논리","tag":"logic","img":"https://images.unsplash.com/photo-1555066931-4365d14bab8c"}
    },
    {
        "q":"사람 돕기 vs 기술 발전",
        "a":{"text":"사람 돕기","tag":"help","img":"https://images.unsplash.com/photo-1526256262350-7da7584cf5eb"},
        "b":{"text":"기술 발전","tag":"logic","img":"https://images.unsplash.com/photo-1518770660439-4636190af475"}
    },
    {
        "q":"자유 vs 규칙",
        "a":{"text":"자유","tag":"freedom","img":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"},
        "b":{"text":"규칙","tag":"stability","img":"https://images.unsplash.com/photo-1521791136064-7986c2920216"}
    },
    {
        "q":"빠름 vs 정확",
        "a":{"text":"빠름","tag":"speed","img":"https://images.unsplash.com/photo-1508385082359-f38ae991e8f2"},
        "b":{"text":"정확","tag":"logic","img":"https://images.unsplash.com/photo-1523966211575-eb4a01e7dd51"}
    },
    {
        "q":"혼자 vs 협업",
        "a":{"text":"혼자","tag":"solo","img":"https://images.unsplash.com/photo-1518770660439-4636190af475"},
        "b":{"text":"협업","tag":"team","img":"https://images.unsplash.com/photo-1522202176988-66273c2fd55f"}
    },
    {
        "q":"재미 vs 돈",
        "a":{"text":"재미","tag":"fun","img":"https://images.unsplash.com/photo-1520975922284-7c4d3c7c8c63"},
        "b":{"text":"돈","tag":"stability","img":"https://images.unsplash.com/photo-1554224154-22dec7ec8818"}
    },
]

# =========================
# 📊 그래프
# =========================
def draw_chart(score):
    fig, ax = plt.subplots()
    ax.bar(score.keys(), score.values(), color="#4f46e5")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =========================
# 🧠 MBTI 계산
# =========================
def get_mbti(score):
    best, best_score = None, 0
    for mbti, traits in mbti_map.items():
        s = sum(score.get(t,0) for t in traits)
        if s > best_score:
            best, best_score = mbti, s
    return best or "INFP"

# =========================
# 🤖 이미지 설명 AI (룰 기반)
# =========================
def explain(tag):
    ai = {
        "solo":"혼자 집중하는 성향이 강합니다. 독립적인 작업을 선호해요.",
        "team":"협업을 좋아하고 사람들과 함께 성장하는 타입입니다.",
        "creative":"창의적인 아이디어를 중요하게 생각합니다.",
        "logic":"논리적이고 분석적인 사고를 합니다.",
        "help":"다른 사람을 돕는 것에서 만족을 느낍니다.",
        "freedom":"자유로운 환경에서 능력이 발휘됩니다.",
        "stability":"안정적이고 계획적인 환경을 선호합니다.",
        "fun":"재미와 흥미를 중요하게 생각합니다.",
        "challenge":"도전을 즐기고 성장 욕구가 강합니다.",
        "speed":"빠른 판단과 실행력을 가지고 있습니다."
    }
    return ai.get(tag,"이 선택은 당신의 성향을 보여줍니다.")

# =========================
# 상태 초기화
# =========================
st.set_page_config(page_title="밸런스 게임 AI")

st.title("🎮 직업 밸런스 게임 + AI 분석")

if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}

# =========================
# 질문 화면
# =========================
if st.session_state.i < len(questions):

    q = questions[st.session_state.i]

    st.subheader(q["q"])

    col1, col2 = st.columns(2)

    with col1:
        st.image(q["a"]["img"], use_container_width=True)
        if st.button(q["a"]["text"]):
            st.session_state.score[q["a"]["tag"]] = st.session_state.score.get(q["a"]["tag"],0)+1
            st.session_state.last = q["a"]["tag"]
            st.session_state.i += 1
            st.rerun()

    with col2:
        st.image(q["b"]["img"], use_container_width=True)
        if st.button(q["b"]["text"]):
            st.session_state.score[q["b"]["tag"]] = st.session_state.score.get(q["b"]["tag"],0)+1
            st.session_state.last = q["b"]["tag"]
            st.session_state.i += 1
            st.rerun()

# =========================
# 🎉 결과 + 애니메이션 + AI 설명
# =========================
else:

    st.success("🎉 결과 분석 중...")

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)

    st.balloons()

    mbti = get_mbti(st.session_state.score)

    # fade-in 효과
    st.markdown("""
    <style>
    .fade {animation: fade 1.2s ease-in;}
    @keyframes fade {
        from {opacity:0; transform:translateY(20px);}
        to {opacity:1; transform:translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fade">', unsafe_allow_html=True)

    st.subheader(f"🧠 MBTI 결과: {mbti}")

    draw_chart(st.session_state.score)

    # 🧠 AI 설명
    st.subheader("🤖 선택 분석 AI")
    if "last" in st.session_state:
        st.write(explain(st.session_state.last))

    # 🐱 고양이
    st.subheader("🐱 당신의 MBTI 고양이")
    if mbti in mbti_cat:
        st.image(mbti_cat[mbti], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 다시 시작"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.session_state.last = None
        st.rerun()
