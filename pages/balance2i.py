import streamlit as st
import matplotlib.pyplot as plt
import time

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="커리어 AI", page_icon="🎮")
st.title("🎮 성향 분석 → 직업 추천 AI")

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
    ("쉬는 시간", "혼자 쉰다", "친구랑 논다", "solo", "team"),
    ("문제 해결", "혼자 생각", "새 방법", "logic", "creative"),
    ("프로젝트", "혼자", "팀", "solo", "team"),
    ("숙제", "빠르게", "꼼꼼하게", "speed", "logic"),
    ("주말", "집", "밖", "stability", "freedom"),
    ("도전", "안정", "도전", "stability", "challenge"),
    ("친구", "적게", "많이", "solo", "team"),
    ("아이디어", "실행", "창의", "logic", "creative"),
]

# =========================
# 직업
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
# 점수 계산
# =========================
def job_score(traits_list, user_score):
    return sum(user_score.get(t,0) for t in traits_list)

# =========================
# AI 설명
# =========================
def ai(job, traits_list):
    return f"""
🤖 AI 분석

📌 {job}

🧠 성향:
{", ".join(traits_list)}

💡 설명:
당신의 성향과 높은 일치도를 보이는 직업입니다.
"""

# =========================
# TOP5 추천
# =========================
def get_top5(user_score):
    scored = []
    for name, t in job_pool:
        s = job_score(t, user_score)
        scored.append((name, s))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:5]

# =========================
# 🎮 QUIZ
# =========================
if st.session_state.stage == "quiz":

    if st.session_state.q_i >= len(questions):
        st.session_state.stage = "wc"

        user_score = st.session_state.score

        scored_jobs = []
        for name, t in job_pool:
            scored_jobs.append({
                "name": name,
                "traits": t,
                "score": job_score(t, user_score)
            })

        scored_jobs.sort(key=lambda x: x["score"], reverse=True)

        st.session_state.top5 = get_top5(user_score)

        st.session_state.wc = scored_jobs[:16]
        st.session_state.next_wc = []
        st.session_state.wc_i = 0

        st.rerun()

    q = questions[st.session_state.q_i]

    st.progress(st.session_state.q_i / len(questions))
    st.subheader("🎮 성향 테스트")

    col1, col2 = st.columns(2)

    if col1.button(q[1]):
        st.session_state.score[q[3]] = st.session_state.score.get(q[3],0)+1
        st.session_state.q_i += 1
        st.rerun()

    if col2.button(q[2]):
        st.session_state.score[q[4]] = st.session_state.score.get(q[4],0)+1
        st.session_state.q_i += 1
        st.rerun()

# =========================
# 🏆 WC (애니메이션 추가)
# =========================
elif st.session_state.stage == "wc":

    wc = st.session_state.wc
    i = st.session_state.wc_i

    st.subheader("🏆 직업 월드컵")

    if len(wc) == 1:
        st.session_state.winner = wc[0]
        st.session_state.stage = "end"
        st.rerun()

    if i >= len(wc) - 1:
        st.session_state.wc = st.session_state.next_wc
        st.session_state.next_wc = []
        st.session_state.wc_i = 0
        st.rerun()

    a = wc[i]
    b = wc[i+1]

    # 🎮 애니메이션 효과
    st.progress(i / len(wc))
    st.markdown("### ⚡ 선택하세요!")

    col1, col2 = st.columns(2)

    if col1.button(f"🔥 {a['name']}"):
        with st.spinner("분석 중..."):
            time.sleep(0.4)
        st.session_state.next_wc.append(a)
        st.session_state.wc_i += 2
        st.rerun()

    if col2.button(f"🔥 {b['name']}"):
        with st.spinner("분석 중..."):
            time.sleep(0.4)
        st.session_state.next_wc.append(b)
        st.session_state.wc_i += 2
        st.rerun()

# =========================
# 🎯 END
# =========================
elif st.session_state.stage == "end":

    st.success("🎯 분석 완료!")

    values = [st.session_state.score.get(t,0) for t in traits]

    fig, ax = plt.subplots()
    ax.bar(traits, values, color="#4f46e5")
    st.pyplot(fig)

    winner = st.session_state.winner

    st.subheader("🏆 최종 직업")
    st.write(winner["name"])

    st.subheader("🏆 TOP 5 추천 직업")

    for name, score in st.session_state.top5:
        st.write(f"⭐ {name} ({score}점)")

    st.subheader("🤖 AI 분석")

    st.markdown(ai(winner["name"], winner["traits"]))

    if st.button("🔄 다시 시작"):
        for k in st.session_state.keys():
            del st.session_state[k]
        st.rerun()
