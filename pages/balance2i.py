import streamlit as st
import matplotlib.pyplot as plt
import random

# =========================
# 설정
# =========================
st.set_page_config(page_title="커리어 게임", page_icon="🎮")

st.title("🎮 성향 밸런스 게임 + 직업 16강")

# =========================
# 성향
# =========================
traits = [
    "solo","team","creative","logic",
    "freedom","stability","challenge",
    "speed","help"
]

# =========================
# 🎮 밸런스 게임 (많게 구성)
# =========================
questions = [
    ("📚 쉬는 시간", "혼자 쉰다", "친구랑 논다", "solo", "team"),
    ("🎮 게임 스타일", "전략 먼저", "일단 부딪힘", "logic", "challenge"),
    ("🍱 점심시간", "조용히 먹는다", "수다 떤다", "solo", "team"),
    ("🧩 문제 해결", "끝까지 혼자", "새 방법 찾기", "logic", "creative"),
    ("📱 방과 후", "집에서 쉰다", "밖에서 논다", "stability", "freedom"),
    ("⚡ 숙제 많을 때", "빠르게 끝냄", "정확하게 함", "speed", "logic"),
    ("👥 발표 수업", "혼자 준비", "팀으로 준비", "solo", "team"),
    ("🚀 어려운 문제", "차근차근 분석", "도전적으로 해결", "logic", "challenge"),
    ("🎨 과제 스타일", "정해진 방식", "자유롭게 창작", "stability", "creative"),
    ("🧠 선택 상황", "안전한 선택", "모험적인 선택", "stability", "challenge"),
    ("🤝 역할", "도와주는 역할", "리드하는 역할", "help", "team"),
    ("⏱ 시간 압박", "빠르게 처리", "천천히 정확하게", "speed", "logic"),
]

# =========================
# 🏆 16강 직업
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

# 랜덤 보정 (16강 유지)
while len(job_pool) < 16:
    job_pool.append(random.choice(job_pool))

jobs = [{"name":j[0], "traits":j[1]} for j in job_pool]
random.shuffle(jobs)

# =========================
# 상태
# =========================
if "q_i" not in st.session_state:
    st.session_state.q_i = 0
    st.session_state.score = {}

if "wc" not in st.session_state:
    st.session_state.wc = jobs
    st.session_state.wc_i = 0
    st.session_state.round = 16
    st.session_state.winner = None

# =========================
# 🎮 1단계: 밸런스 게임
# =========================
if st.session_state.q_i < len(questions):

    q = questions[st.session_state.q_i]

    st.progress(st.session_state.q_i / len(questions))
    st.subheader("🎮 성향 밸런스 게임")

    st.write(q[0])

    col1, col2 = st.columns(2)

    if col1.button(q[1]):
        st.session_state.score[q[3]] = st.session_state.score.get(q[3],0) + 1
        st.session_state.q_i += 1
        st.rerun()

    if col2.button(q[2]):
        st.session_state.score[q[4]] = st.session_state.score.get(q[4],0) + 1
        st.session_state.q_i += 1
        st.rerun()

# =========================
# 🏆 2단계: 16강 월드컵
# =========================
elif st.session_state.winner is None:

    wc = st.session_state.wc
    i = st.session_state.wc_i

    st.subheader(f"🏆 직업 이상형 월드컵 ({st.session_state.round}강)")

    # 종료
    if len(wc) == 1:
        st.session_state.winner = wc[0]
        st.rerun()

    # 라운드 종료
    if i >= len(wc) - 1:
        wc = wc[:len(wc)//2]
        st.session_state.wc = wc
        st.session_state.wc_i = 0
        st.session_state.round = len(wc)
        st.rerun()

    a = wc[i]
    b = wc[i+1]

    st.write("더 끌리는 직업 선택 👇")

    col1, col2 = st.columns(2)

    if col1.button(a["name"]):
        wc.append(a)
        st.session_state.wc_i += 2
        st.rerun()

    if col2.button(b["name"]):
        wc.append(b)
        st.session_state.wc_i += 2
        st.rerun()

# =========================
# 🧠 3단계: 결과
# =========================
else:

    st.success("🎯 분석 완료!")

    # =========================
    # 성향 그래프
    # =========================
    st.subheader("🧠 성향 분석")

    values = [st.session_state.score.get(t,0) for t in traits]

    fig, ax = plt.subplots()
    ax.bar(traits, values, color="#4f46e5")
    st.pyplot(fig)

    # =========================
    # 성향 설명
    # =========================
    st.subheader("🤖 너의 성향")

    explain = {
        "solo":"혼자 집중하는 스타일",
        "team":"협업 좋아하는 스타일",
        "logic":"논리적으로 생각하는 스타일",
        "creative":"창의적인 스타일",
        "freedom":"자유로운 스타일",
        "stability":"안정적인 스타일",
        "challenge":"도전 좋아하는 스타일",
        "speed":"빠른 실행 스타일",
        "help":"도와주는 스타일"
    }

    top = sorted(st.session_state.score.items(), key=lambda x: x[1], reverse=True)[:3]

    for t,_ in top:
        st.write("👉", explain.get(t))

    # =========================
    # 🏆 TOP 5 직업
    # =========================
    st.subheader("💼 TOP 5 직업")

    scores = []
    for name, traits_list in job_pool:
        score = sum(st.session_state.score.get(t,0) for t in traits_list)
        scores.append((name, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    for name, score in scores[:5]:
        st.write(f"⭐ {name} ({score:.1f})")

    # =========================
    # 🏆 최종 직업
    # =========================
    st.subheader("🏆 최종 선택 직업")

    st.write(st.session_state.winner["name"])

    # =========================
    # 🔄 다시 시작
    # =========================
    if st.button("🔄 다시 시작"):
        st.session_state.q_i = 0
        st.session_state.score = {}

        jobs = [{"name":j[0], "traits":j[1]} for j in job_pool]
        random.shuffle(jobs)

        st.session_state.wc = jobs
        st.session_state.wc_i = 0
        st.session_state.round = 16
        st.session_state.winner = None

        st.rerun()
