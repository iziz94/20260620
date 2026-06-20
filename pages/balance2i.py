import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# =========================
# 페이지
# =========================
st.set_page_config(page_title="커리어 월드컵", page_icon="🎮")

st.title("🎮 성향 분석 + 32강 직업 월드컵")

# =========================
# 성향
# =========================
traits = [
    "solo","team","creative","logic",
    "help","freedom","stability",
    "challenge","speed"
]

# =========================
# 🎮 밸런스 게임 질문
# =========================
questions = [
    ("혼자 해결 vs 팀 해결", "solo", "team"),
    ("논리 vs 창의", "logic", "creative"),
    ("안정 vs 도전", "stability", "challenge"),
    ("자유 vs 규칙", "freedom", "stability"),
    ("빠름 vs 정확", "speed", "logic"),
    ("혼자 집중 vs 협업", "solo", "team"),
    ("도움 vs 리더", "help", "team"),
    ("새로운 시도 vs 익숙한 방법", "challenge", "stability"),
    ("혼자 일 vs 사람과 일", "solo", "team"),
    ("아이디어 vs 실행", "creative", "logic"),
]

# =========================
# 🏆 32강 직업 데이터
# =========================
job_pool = [
    ("소프트웨어 엔지니어", ["logic","solo"]),
    ("데이터 분석가", ["logic","solo"]),
    ("AI 연구원", ["logic","creative"]),
    ("보안 전문가", ["logic","solo"]),
    ("UX 디자이너", ["creative"]),
    ("그래픽 디자이너", ["creative"]),
    ("영상 편집자", ["creative","freedom"]),
    ("유튜버", ["creative","freedom"]),
    ("마케터", ["creative","team"]),
    ("브랜드 매니저", ["team","creative"]),
    ("기획자", ["team","logic"]),
    ("프로덕트 매니저", ["logic","team"]),
    ("창업가", ["challenge","freedom"]),
    ("스타트업 CEO", ["challenge","team"]),
    ("교사", ["help","team"]),
    ("상담사", ["help"]),
    ("간호사", ["help","team"]),
    ("의사", ["logic","help"]),
    ("변호사", ["logic"]),
    ("회계사", ["logic","stability"]),
    ("공무원", ["stability"]),
    ("군인", ["discipline","stability"]),
    ("경찰", ["help","discipline"]),
    ("건축가", ["creative","logic"]),
    ("데이터 엔지니어", ["logic"]),
    ("게임 개발자", ["creative","logic"]),
    ("애니메이터", ["creative"]),
    ("작가", ["creative","solo"]),
    ("번역가", ["solo","logic"]),
    ("심리학자", ["help","logic"]),
    ("영업 전문가", ["team","speed"]),
    ("비즈니스 컨설턴트", ["logic","team"]),
]

# =========================
# 상태
# =========================
if "q_i" not in st.session_state:
    st.session_state.q_i = 0
    st.session_state.score = {}

if "wc" not in st.session_state:
    jobs = [{"name":j[0], "traits":j[1]} for j in job_pool]
    random.shuffle(jobs)
    st.session_state.wc = jobs
    st.session_state.wc_i = 0
    st.session_state.round = 32
    st.session_state.winner = None

# =========================
# 🎮 1. 성향 게임
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
# 🏆 2. 32강 월드컵
# =========================
elif st.session_state.winner is None:

    wc = st.session_state.wc
    i = st.session_state.wc_i

    st.subheader(f"🏆 직업 월드컵 ({st.session_state.round}강)")

    # 1개 남으면 우승
    if len(wc) == 1:
        st.session_state.winner = wc[0]
        st.rerun()

    # 인덱스 보호
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
# 🧠 3. 결과 + TOP5
# =========================
else:

    st.success("🎯 결과 완료!")

    # =========================
    # 성향 그래프
    # =========================
    st.subheader("🧠 성향 분석")

    values = [st.session_state.score.get(t,0) for t in traits]

    fig, ax = plt.subplots()
    ax.bar(traits, values, color="#4f46e5")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # =========================
    # TOP 성향 설명
    # =========================
    st.subheader("🤖 성향 설명")

    explain = {
        "solo":"혼자 집중형",
        "team":"협업형",
        "logic":"논리형",
        "creative":"창의형",
        "freedom":"자유형",
        "stability":"안정형",
        "challenge":"도전형",
        "speed":"속도형",
        "help":"도움형"
    }

    top_traits = sorted(st.session_state.score.items(), key=lambda x: x[1], reverse=True)[:3]

    for t,_ in top_traits:
        st.write("👉", explain.get(t))

    # =========================
    # 🏆 TOP 5 직업 추천
    # =========================
    st.subheader("💼 TOP 5 직업 추천")

    job_scores = []

    for name, traits_list in job_pool:
        score = sum(st.session_state.score.get(t,0) for t in traits_list)
        job_scores.append((name, score))

    job_scores.sort(key=lambda x: x[1], reverse=True)

    top5 = job_scores[:5]

    for name, score in top5:
        st.write(f"⭐ {name} ({score:.1f}점)")

    # =========================
    # 🏆 최종 월드컵 우승
    # =========================
    st.subheader("🏆 최종 선택 직업")

    winner = st.session_state.winner

    st.write("💼", winner["name"])

    # =========================
    # 🔄 재시작
    # =========================
    if st.button("🔄 다시 시작"):
        st.session_state.q_i = 0
        st.session_state.score = {}

        jobs = [{"name":j[0], "traits":j[1]} for j in job_pool]
        random.shuffle(jobs)

        st.session_state.wc = jobs
        st.session_state.wc_i = 0
        st.session_state.round = 32
        st.session_state.winner = None

        st.rerun()
