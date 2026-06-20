import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# 직업 데이터 (50개)
# -----------------------------
jobs = [
    {"name": "소프트웨어 개발자", "tags": ["tech", "logic", "solo"], "desc": "앱과 프로그램 개발"},
    {"name": "게임 개발자", "tags": ["tech", "creative", "fun"], "desc": "게임 제작"},
    {"name": "의사", "tags": ["help", "precision"], "desc": "환자 치료"},
    {"name": "간호사", "tags": ["help", "team"], "desc": "환자 케어"},
    {"name": "교사", "tags": ["help", "structure"], "desc": "교육"},
    {"name": "유튜버", "tags": ["creative", "freedom"], "desc": "콘텐츠 제작"},
    {"name": "디자이너", "tags": ["creative"], "desc": "시각 디자인"},
    {"name": "데이터 분석가", "tags": ["logic", "tech"], "desc": "데이터 분석"},
    {"name": "AI 연구원", "tags": ["logic", "tech", "challenge"], "desc": "AI 연구"},
    {"name": "경찰", "tags": ["stability", "field"], "desc": "치안 유지"},
    {"name": "소방관", "tags": ["help", "field"], "desc": "화재 진압"},
    {"name": "군인", "tags": ["stability"], "desc": "국방"},
    {"name": "요리사", "tags": ["creative", "field"], "desc": "요리"},
    {"name": "작가", "tags": ["creative", "solo"], "desc": "글쓰기"},
    {"name": "기자", "tags": ["freedom", "challenge"], "desc": "취재"},
    {"name": "변호사", "tags": ["logic", "challenge"], "desc": "법률"},
    {"name": "회계사", "tags": ["logic", "precision"], "desc": "회계"},
    {"name": "연구원", "tags": ["solo", "logic"], "desc": "연구"},
    {"name": "파일럿", "tags": ["precision"], "desc": "비행"},
    {"name": "승무원", "tags": ["team", "help"], "desc": "서비스"},
    {"name": "마케터", "tags": ["creative", "team"], "desc": "홍보"},
    {"name": "창업가", "tags": ["challenge", "freedom"], "desc": "사업"},
    {"name": "영상 편집자", "tags": ["creative", "tech"], "desc": "영상 제작"},
    {"name": "사진작가", "tags": ["creative"], "desc": "촬영"},
    {"name": "건축가", "tags": ["logic", "creative"], "desc": "건물 설계"},
    {"name": "엔지니어", "tags": ["logic", "tech"], "desc": "기술 설계"},
    {"name": "로봇공학자", "tags": ["tech", "challenge"], "desc": "로봇 개발"},
    {"name": "심리상담사", "tags": ["help"], "desc": "상담"},
    {"name": "환경과학자", "tags": ["logic", "field"], "desc": "환경 연구"},
    {"name": "UI 디자이너", "tags": ["creative", "tech"], "desc": "UI 설계"},
    {"name": "UX 디자이너", "tags": ["creative", "logic"], "desc": "UX 설계"},
    {"name": "데이터 사이언티스트", "tags": ["logic", "tech"], "desc": "데이터 분석"},
]

# -----------------------------
# 질문
# -----------------------------
questions = [
    ("혼자 vs 팀", "solo", "team"),
    ("안정 vs 도전", "stability", "challenge"),
    ("예술 vs 논리", "creative", "logic"),
    ("사람 도움 vs 기술", "help", "tech"),
    ("빠름 vs 정확", "speed", "precision"),
    ("회사 vs 창업", "stability", "challenge"),
    ("계획 vs 자유", "structure", "freedom"),
    ("현장 vs 컴퓨터", "field", "tech"),
    ("재미 vs 돈", "fun", "money"),
    ("혼자 vs 협업", "solo", "team"),
]

# -----------------------------
# AI 스타일 설명 생성 (룰 기반)
# -----------------------------
def ai_description(job, score):
    top_tags = sorted(score.items(), key=lambda x: x[1], reverse=True)[:2]

    desc = f"""
당신은 '{job}' 유형과 높은 적합성을 보입니다.

핵심 성향:
"""

    for t, v in top_tags:
        desc += f"- {t} 성향이 강함 ({v}점)\n"

    desc += f"""
이 직업은 당신의 성향과 잘 맞으며,
문제 해결 능력과 적응력이 중요한 분야입니다.

AI 분석 결과: 높은 적합도 예상 🚀
"""
    return desc

# -----------------------------
# 성향 그래프
# -----------------------------
def draw_chart(score):
    if not score:
        return

    labels = list(score.keys())
    values = list(score.values())

    fig, ax = plt.subplots()
    ax.bar(labels, values, color="#4f46e5")
    ax.set_title("직업 성향 분석")
    plt.xticks(rotation=45)

    st.pyplot(fig)

# -----------------------------
# 계산
# -----------------------------
def get_results(score):
    results = []

    for job in jobs:
        match = 0
        for t in job["tags"]:
            match += score.get(t, 0)

        results.append({
            "name": job["name"],
            "desc": job["desc"],
            "score": match
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)[:10]

# -----------------------------
# Streamlit 설정
# -----------------------------
st.set_page_config(page_title="직업 AI 테스트", layout="centered")

st.title("🎮 직업 밸런스 + AI 분석 시스템")

if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = {}

# -----------------------------
# 질문
# -----------------------------
if st.session_state.i < len(questions):
    q = questions[st.session_state.i]

    st.subheader(q[0])

    col1, col2 = st.columns(2)

    if col1.button("A"):
        st.session_state.score[q[1]] = st.session_state.score.get(q[1], 0) + 1
        st.session_state.i += 1
        st.rerun()

    if col2.button("B"):
        st.session_state.score[q[2]] = st.session_state.score.get(q[2], 0) + 1
        st.session_state.i += 1
        st.rerun()

# -----------------------------
# 결과
# -----------------------------
else:
    st.subheader("🔍 당신의 직업 성향 그래프")
    draw_chart(st.session_state.score)

    st.subheader("🔥 TOP 10 직업")

    results = get_results(st.session_state.score)

    for i, r in enumerate(results):
        st.markdown(f"""
### {i+1}. {r['name']}
- {r['desc']}
- 점수: {r['score']}

🤖 AI 분석:
{ai_description(r['name'], st.session_state.score)}
        """)

    if st.button("다시 시작"):
        st.session_state.i = 0
        st.session_state.score = {}
        st.rerun()
