import streamlit as st
import matplotlib.pyplot as plt
import random

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="커리어 게임", page_icon="🎮")
st.title("🎮 성향 → 직업 월드컵")

# =========================
# 상태 초기화
# =========================
if "stage" not in st.session_state:
    st.session_state.stage = "quiz"

if "q_i" not in st.session_state:
    st.session_state.q_i = 0
    st.session_state.score = {}

if "wc" not in st.session_state:
    st.session_state.wc = []

if "next_wc" not in st.session_state:
    st.session_state.next_wc = []

if "wc_i" not in st.session_state:
    st.session_state.wc_i = 0

if "winner" not in st.session_state:
    st.session_state.winner = None

# =========================
# 성향
# =========================
traits = [
    "solo","team","creative","logic",
    "freedom","stability","challenge",
    "speed","help"
]

# =========================
# 질문
# =========================
questions = [
    ("📚 쉬는 시간", "혼자 쉰다", "친구랑 논다", "solo", "team"),
    ("🎮 게임 스타일", "전략형", "즉흥형", "logic", "challenge"),
    ("🍱 점심시간", "혼자 먹는다", "같이 먹는다", "solo", "team"),
    ("🧩 문제 해결", "혼자 해결", "새 방법 찾기", "logic", "creative"),
    ("📱 방과 후", "집에서 쉰다", "밖에서 논다", "stability", "freedom"),
    ("⚡ 시간 부족", "빠르게 끝냄", "정확하게", "speed", "logic"),
    ("👥 발표", "혼자", "팀", "solo", "team"),
    ("🚀 문제 해결", "분석", "도전", "logic", "challenge"),
    ("🎨 과제", "정형", "자유", "stability", "creative"),
    ("🤝 역할", "도움", "리더", "help", "team"),
]

# =========================
# 직업 (16강)
# =========================
job_pool = [
    ("소프트웨어 엔지니어", ["logic","solo"]),
    ("데이터 분석가", ["logic","solo"]),
    ("AI 연구원", ["logic","creative"]),
    ("UX 디자이너", ["creative"]),
    ("그래픽 디자이너", ["creative"]),
    ("유튜버", ["creative","freedom"]),
    ("마케터", ["creative","team"]),
    ("기획자", ["team","logic"]),
    ("PM", ["team","logic"]),
    ("창업가", ["challenge","freedom"]),
    ("교사", ["help","team"]),
    ("상담사", ["help"]),
    ("의사", ["logic","help"]),
    ("변호사", ["logic"]),
    ("회계사", ["logic","stability"]),
    ("공무원", ["stability"]),
]

# =========================
# 🎮 1. 성향 테스트
# =========================
if st.session_state.stage == "quiz":

    if st.session_state.q_i >= len(questions):
        st.session_state.stage = "wc"

        # 🔥 월드컵 생성 (여기서 딱 1번)
        jobs = [{"name":j[0], "traits":j[1]} for j in job_pool]
        random.shuffle(jobs)

        st.session_state.wc = jobs
        st.session_state.next_wc = []
        st.session_state.wc_i = 0

        st.rerun()

    q = questions[st.session_state.q_i]

    st.progress(st.session_state.q_i / len(questions))
    st.subheader("🎮 성향 밸런스 게임")
    st.write(q[0])

    col1, col2 = st.columns(2)

    if col1.button(q[1]):
        st.session_state.score[q[3]] = st.session_state.score.get(q[3], 0) + 1
        st.session_state.q_i += 1
        st.rerun()

    if col2.button(q[2]):
        st.session_state.score[q[4]] = st.session_state.score.get(q[4], 0) + 1
        st.session_state.q_i += 1
        st.rerun()

# =========================
# 🏆 2. 직업 월드컵 (16강)
# =========================
elif st.session_state.stage == "wc":

    wc = st.session_state.wc
    i = st.session_state.wc_i

    st.subheader("🏆 직업 16강 월드컵")

    # 종료 조건 (1명 남으면 끝)
    if len(wc) == 1:
        st.session_state.winner = wc[0]
        st.session_state.stage = "end"
        st.rerun()

    # 라운드 종료 (다 돌았으면 교체)
    if i >= len(wc) - 1:
        st.session_state.wc = st.session_state.next_wc
        st.session_state.next_wc = []
        st.session_state.wc_i = 0
        st.rerun()

    a = wc[i]
    b = wc[i + 1]

    col1, col2 = st.columns(2)

    # 선택 1
    if col1.button(a["name"]):
        st.session_state.next_wc.append(a)
        st.session_state.wc_i += 2
        st.rerun()

    # 선택 2
    if col2.button(b["name"]):
        st.session_state.next_wc.append(b)
        st.session_state.wc_i += 2
        st.rerun()

# =========================
# 🎯 3. 결과
# =========================
elif st.session_state.stage == "end":

    st.success("🎯 분석 완료!")

    values = [st.session_state.score.get(t, 0) for t in traits]

    fig, ax = plt.subplots()
    ax.bar(traits, values, color="#4f46e5")
    st.pyplot(fig)

    st.subheader("🏆 최종 직업")
    st.write(st.session_state.winner["name"])

    # =========================
    # 성향 분석
    # =========================
    st.subheader("🧠 성향 TOP")

    top = sorted(st.session_state.score.items(), key=lambda x: x[1], reverse=True)[:3]
    for t, v in top:
        st.write("👉", t)

    # =========================
    # 다시 시작
    # =========================
    if st.button("🔄 다시 시작"):

        st.session_state.stage = "quiz"
        st.session_state.q_i = 0
        st.session_state.score = {}

        st.session_state.wc = []
        st.session_state.next_wc = []
        st.session_state.wc_i = 0
        st.session_state.winner = None

        st.rerun()
