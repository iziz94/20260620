
import streamlit as st
import matplotlib.pyplot as plt
import time

# =========================
# 🎨 버튼 애니메이션 CSS
# =========================
st.markdown("""
<style>
.stButton button {
    width: 100%;
    height: 60px;
    font-size: 18px;
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
# 🧠 MBTI → 고양이
# =========================
mbti_cat = {
    "INTJ":"https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "INTP":"https://images.unsplash.com/photo-1533738363-b7f9aef128ce",
    "ENTJ":"https://images.unsplash.com/photo-1543852786-1cf6624b9987",
    "ENTP":"https://images.unsplash.com/photo-1543852786-1cf6624b9987",

    "INFJ":"https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "INFP":"https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "ENFJ":"https://images.unsplash.com/photo-1552053831-71594a27632d",
    "ENFP":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",

    "ISTJ":"https://images.unsplash.com/photo-1511044568932-338cba0ad803",
    "ISFJ":"https://images.unsplash.com/photo-1511044568932-338cba0ad803",
    "ESTJ":"https://images.unsplash.com/photo-1521791136064-7986c2920216",
    "ESFJ":"https://images.unsplash.com/photo-1522202176988-66273c2fd55f",

    "ISTP":"https://images.unsplash.com/photo-1521737604893-d14cc237f11d",
    "ISFP":"https://images.unsplash.com/photo-1543852786-1cf6624b9987",
    "ESTP":"https://images.unsplash.com/photo-1508385082359-f38ae991e8f2",
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
    "ENFJ":["help","team","structure"],
    "ENFP":["creative","freedom","fun"],

    "ISTJ":["stability","structure","logic"],
    "ISFJ":["help","structure","team"],
    "ESTJ":["stability","structure","team"],
    "ESFJ":["team","help","fun"],

    "ISTP":["logic","solo","field"],
    "ISFP":["creative","solo","freedom"],
    "ESTP":["speed","challenge","fun"],
    "ESFP":["fun","team","freedom"],
}

# =========================
# 🎮 16문항 밸런스 게임
# =========================
questions = [
    ("혼자 공부 vs 팀 공부", ("혼자","solo"), ("팀","team")),
    ("안정 vs 도전", ("안정","stability"), ("도전","challenge")),
    ("창작 vs 논리", ("창작","creative"), ("논리","logic")),
    ("현장 vs 분석", ("현장","field"), ("분석","logic")),
    ("도움 vs 기술", ("도움","help"), ("기술","logic")),
    ("자유 vs 규칙", ("자유","freedom"), ("규칙","stability")),
    ("빠름 vs 정확", ("빠름","speed"), ("정확","logic")),
    ("혼자 vs 협업", ("혼자","solo"), ("협업","team")),
    ("돈 vs 재미", ("돈","stability"), ("재미","fun")),
    ("아이디어 vs 실행", ("아이디어","creative"), ("실행","logic")),
    ("연구 vs 소통", ("연구","solo"), ("소통","team")),
    ("위험 vs 안정", ("위험","challenge"), ("안정","stability")),
    ("콘텐츠 vs 개발", ("콘텐츠","creative"), ("개발","logic")),
    ("빠른 판단 vs 신중", ("빠름","speed"), ("신중","logic")),
    ("자율 vs 조직", ("자율","freedom"), ("조직","stability")),
    ("혼자 작업 vs 팀 작업", ("혼자","solo"), ("팀","team")),
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
# 상태 초기화
# =========================
st.set_page_config(page_title="밸런스 게임")

st.title("🎮 직업 밸런스 게임 16문항")

if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}

# =========================
# 질문 화면
# =========================
if st.session_state.i < len(questions):

    q = questions[st.session_state.i]

    st.image("https://images.unsplash.com/photo-1521737604893-d14cc237f11d", use_container_width=True)

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
# 🎉 결과 애니메이션
# =========================
else:

    st.success("🎉 결과 생성 중...")

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)

    st.balloons()

    mbti = get_mbti(st.session_state.score)
    cat = mbti_cat.get(mbti)

    # fade-in
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

    st.subheader("🐱 당신의 MBTI 고양이")

    if cat:
        st.image(cat, use_container_width=True)
        st.write(f"당신은 **{mbti} 타입 고양이**입니다 🐾")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 다시 시작"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.rerun()
