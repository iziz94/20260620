import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =========================
# 설정
# =========================
st.set_page_config(page_title="커리어 게임", page_icon="🎮")

st.title("🎮 성향 밸런스 게임 + 직업 월드컵")

# =========================
# 성향
# =========================
traits = [
    "solo","team","creative","logic","help",
    "freedom","stability","challenge","speed"
]

# =========================
# 🎮 밸런스 게임 질문
# =========================
questions = [
    ("혼자 해결 vs 친구와 해결", "solo", "team"),
    ("논리적으로 해결 vs 아이디어로 해결", "logic", "creative"),
    ("안정적인 길 vs 도전적인 길", "stability", "challenge"),
    ("자유롭게 일하기 vs 규칙적인 환경", "freedom", "stability"),
    ("빠르게 처리 vs 정확하게 처리", "speed", "logic"),
    ("혼자 집중 vs 협업", "solo", "team"),
    ("도와주는 역할 vs 중심 역할", "help", "team"),
    ("새로운 시도 vs 익숙한 방법", "challenge", "stability"),
]

# =========================
# 직업 데이터 (월드컵용)
# =========================
jobs = [
    {"name":"소프트웨어 엔지니어","traits":["logic","solo"],"desc":"앱과 시스템 개발"},
    {"name":"데이터 분석가","traits":["logic","solo"],"desc":"데이터 분석 전문가"},
    {"name":"UX 디자이너","traits":["creative"],"desc":"사용자 경험 디자인"},
    {"name":"마케터","traits":["creative","team"],"desc":"브랜드 홍보"},
    {"name":"기획자","traits":["team","logic"],"desc":"서비스 설계"},
    {"name":"창업가","traits":["challenge","freedom"],"desc":"사업가"},
    {"name":"교사","traits":["help","team"],"desc":"교육 전문가"},
    {"name":"유튜버","traits":["creative","freedom"],"desc":"콘텐츠 제작자"},
]

# =========================
# 상태
# =========================
if "q_i" not in st.session_state:
    st.session_state.q_i = 0
    st.session_state.score = {}

if "wc_i" not in st.session_state:
    st.session_state.wc_i = 0
    st.session_state.wc_round = jobs.copy()
    st.session_state.winner = None

# =========================
# 1️⃣ 성향 밸런스 게임
# =========================
if st.session_state.q_i < len(questions):

    q = questions[st.session_state.q_i]

    st.progress(st.session_state.q_i / len(questions))
    st.subheader("🎮 성향 밸런스 게임")
    st.write(q[0])

    col1, col2 = st.columns(2)

    if col1.button(q[1]):
        st.session_state.score[q[1]] = st.session_state.score.get(q[1],0) + 1
        st.session_state.q_i += 1
        st.rerun()

    if col2.button(q[2]):
        st.session_state.score[q[2]] = st.session_state.score.get(q[2],0) + 1
        st.session_state.q_i += 1
        st.rerun()

# =========================
# 2️⃣ 직업 이상형 월드컵
# =========================
elif st.session_state.winner is None:

    round_list = st.session_state.wc_round
    i = st.session_state.wc_i

    if len(round_list) == 1:
        st.session_state.winner = round_list[0]
        st.rerun()

    a = round_list[i]
    b = round_list[i+1]

    st.subheader("🏆 직업 이상형 월드컵")
    st.write("더 끌리는 직업을 선택하세요")

    col1, col2 = st.columns(2)

    if col1.button(a["name"]):
        round_list.append(a)
        st.session_state.wc_i += 2
        st.rerun()

    if col2.button(b["name"]):
        round_list.append(b)
        st.session_state.wc_i += 2
        st.rerun()

    # 다음 라운드
    if st.session_state.wc_i >= len(round_list):
        st.session_state.wc_round = round_list[len(round_list)//2:]
        st.session_state.wc_i = 0
        st.rerun()

# =========================
# 3️⃣ 결과
# =========================
else:

    st.success("🎯 결과 완료!")

    # =========================
    # 성향 분석
    # =========================
    st.subheader("🧠 성향 결과")

    values = [st.session_state.score.get(t,0) for t in traits]

    fig, ax = plt.subplots()
    ax.bar(traits, values)
    st.pyplot(fig)

    # =========================
    # AI 설명
    # =========================
    st.subheader("🤖 성향 설명")

    top = sorted(st.session_state.score.items(), key=lambda x: x[1], reverse=True)[:3]

    explain = {
        "solo":"혼자 집중하는 스타일",
        "team":"사람들과 협업하는 스타일",
        "logic":"논리적으로 생각하는 스타일",
        "creative":"창의적인 스타일",
        "freedom":"자유를 좋아하는 스타일",
        "stability":"안정적인 걸 좋아하는 스타일",
        "challenge":"도전을 좋아하는 스타일",
        "speed":"빠른 판단 스타일",
        "help":"도와주는 스타일"
    }

    for t, _ in top:
        st.write("👉", explain.get(t,""))

    # =========================
    # 최종 직업
    # =========================
    job = st.session_state.winner

    st.subheader("🏆 최종 직업")

    st.write("💼", job["name"])
    st.write("🧠", job["desc"])

    # =========================
    # 다시 시작
    # =========================
    if st.button("🔄 다시 시작"):
        st.session_state.q_i = 0
        st.session_state.wc_i = 0
        st.session_state.score = {}
        st.session_state.wc_round = jobs.copy()
        st.session_state.winner = None
        st.rerun()
