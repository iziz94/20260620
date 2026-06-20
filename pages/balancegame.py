import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# MBTI 매핑 (간단 버전)
# -----------------------------
mbti_map = {
    "INTJ": ["logic", "solo", "structure"],
    "INTP": ["logic", "solo", "creative"],
    "ENTJ": ["challenge", "logic", "team"],
    "ENFP": ["creative", "freedom", "fun"],
    "INFJ": ["help", "solo", "structure"],
    "INFP": ["creative", "solo", "freedom"],
    "ESTJ": ["stability", "structure", "team"],
    "ESFP": ["fun", "freedom", "team"],
}

# -----------------------------
# 직업 데이터 (축약 50개)
# -----------------------------
jobs = [
    {"name": "개발자", "tags": ["tech", "logic", "solo"], "desc": "앱/프로그램 개발"},
    {"name": "게임 개발자", "tags": ["tech", "creative", "fun"], "desc": "게임 제작"},
    {"name": "의사", "tags": ["help", "precision"], "desc": "환자 치료"},
    {"name": "교사", "tags": ["help", "structure"], "desc": "교육"},
    {"name": "유튜버", "tags": ["creative", "freedom", "fun"], "desc": "콘텐츠 제작"},
    {"name": "디자이너", "tags": ["creative"], "desc": "디자인"},
    {"name": "데이터 분석가", "tags": ["logic", "tech"], "desc": "데이터 분석"},
    {"name": "AI 연구원", "tags": ["logic", "tech", "challenge"], "desc": "AI 연구"},
    {"name": "경찰", "tags": ["stability", "team"], "desc": "치안"},
    {"name": "소방관", "tags": ["help", "field"], "desc": "구조 활동"},
    {"name": "작가", "tags": ["creative", "solo"], "desc": "글쓰기"},
    {"name": "기자", "tags": ["freedom", "challenge"], "desc": "취재"},
    {"name": "변호사", "tags": ["logic", "challenge"], "desc": "법률"},
    {"name": "회계사", "tags": ["logic", "precision"], "desc": "회계"},
    {"name": "창업가", "tags": ["challenge", "freedom"], "desc": "사업 운영"},
    {"name": "건축가", "tags": ["logic", "creative"], "desc": "건물 설계"},
]

# -----------------------------
# 질문 (이미지 포함)
# -----------------------------
questions = [
    {
        "q": "혼자 일 vs 팀",
        "a": ("혼자", "solo"),
        "b": ("팀", "team"),
        "img": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"
    },
    {
        "q": "안정 vs 도전",
        "a": ("안정", "stability"),
        "b": ("도전", "challenge"),
        "img": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f"
    },
    {
        "q": "예술 vs 논리",
        "a": ("예술", "creative"),
        "b": ("논리", "logic"),
        "img": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97"
    },
    {
        "q": "현장 vs 컴퓨터",
        "a": ("현장", "field"),
        "b": ("컴퓨터", "tech"),
        "img": "https://images.unsplash.com/photo-1581091870622-1e7a2e1f0b3f"
    },
    {
        "q": "돈 vs 재미",
        "a": ("돈", "stability"),
        "b": ("재미", "fun"),
        "img": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c"
    },
]

# -----------------------------
# MBTI 계산
# -----------------------------
def get_mbti(score):
    best = None
    best_match = 0

    for mbti, traits in mbti_map.items():
        match = sum(score.get(t, 0) for t in traits)
        if match > best_match:
            best_match = match
            best = mbti

    return best or "INFP"

# -----------------------------
# 직업 TOP5
# -----------------------------
def get_jobs(score):
    results = []

    for job in jobs:
        match = sum(score.get(t, 0) for t in job["tags"])
        results.append({**job, "score": match})

    return sorted(results, key=lambda x: x["score"], reverse=True)[:5]

# -----------------------------
# 그래프
# -----------------------------
def draw_chart(score):
    if not score:
        return

    fig, ax = plt.subplots()
    ax.bar(score.keys(), score.values(), color="#4f46e5")
    ax.set_title("직업 성향 분석")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -----------------------------
# 초기 설정
# -----------------------------
st.set_page_config(page_title="직업 MBTI 게임", layout="centered")

st.title("🎮 직업 밸런스 + MBTI 분석")

if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}

# -----------------------------
# 질문 화면
# -----------------------------
if st.session_state.i < len(questions):
    q = questions[st.session_state.i]

    st.image(q["img"], use_container_width=True)
    st.subheader(q["q"])

    col1, col2 = st.columns(2)

    if col1.button(q["a"][0]):
        st.session_state.score[q["a"][1]] = st.session_state.score.get(q["a"][1], 0) + 1
        st.session_state.i += 1
        st.rerun()

    if col2.button(q["b"][0]):
        st.session_state.score[q["b"][1]] = st.session_state.score.get(q["b"][1], 0) + 1
        st.session_state.i += 1
        st.rerun()

# -----------------------------
# 결과 화면
# -----------------------------
else:
    st.subheader("📊 당신의 성향 그래프")
    draw_chart(st.session_state.score)

    mbti = get_mbti(st.session_state.score)

    st.subheader(f"🧠 당신의 MBTI 추정: {mbti}")

    st.write("MBTI 기반 성향 분석 결과입니다.")

    st.subheader("🏆 TOP 5 직업 추천")

    for i, job in enumerate(get_jobs(st.session_state.score)):
        st.markdown(f"""
### {i+1}. {job['name']}
- {job['desc']}
- 점수: {job['score']}
        """)

    if st.button("다시하기"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.rerun()
