import streamlit as st
import matplotlib.pyplot as plt
import random
import time

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="진로 게임", page_icon="🎮")
st.title("🎮 나의 미래 직업 찾기 게임")

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
traits = ["solo","team","creative","logic","freedom","stability","challenge","speed","help"]

# =========================
# 🎮 스토리형 질문 (중학생 버전)
# =========================
questions = [
    ("📚 수업 중 발표 상황", 
     "A) 혼자 정리해서 발표한다", "B) 친구랑 같이 준비한다", "solo", "team"),

    ("🎮 게임을 할 때", 
     "A) 전략 세우고 이기려고 한다", "B) 그냥 재미있게 즐긴다", "logic", "freedom"),

    ("🏫 수행평가 숙제", 
     "A) 빨리 끝내고 다른 거 한다", "B) 꼼꼼하게 완벽하게 한다", "speed", "stability"),

    ("👥 친구랑 의견 충돌", 
     "A) 내 생각을 끝까지 말한다", "B) 맞춰서 조율한다", "challenge", "team"),

    ("📱 단톡방 상황", 
     "A) 내가 정리해서 결론 낸다", "B) 조용히 의견을 따른다", "logic", "help"),

    ("🎨 자유 과제", 
     "A) 완전히 내 스타일로 한다", "B) 예시대로 따라 한다", "creative", "stability"),

    ("🚀 새로운 프로젝트", 
     "A) 내가 리드한다", "B) 누군가 시키는 걸 한다", "challenge", "help"),

    ("⏰ 시간이 부족할 때", 
     "A) 빠르게 끝낸다", "B) 천천히 정확하게 한다", "speed", "logic"),
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
def job_score(job_traits, user_score):
    return sum(user_score.get(t, 0) for t in job_traits)

# =========================
# AI 설명
# =========================
def ai_explain(job, traits_list):
    return f"""
🤖 AI 분석

📌 직업: {job}

🧠 이 직업의 핵심 특징:
{", ".join(traits_list)}

💡 설명:
이 직업은 당신의 성향과 잘 맞는 직업입니다.
특히 해당 성향이 자연스럽게 발휘됩니다.

🚀 추천 이유:
이 직업 환경에서 가장 편하게 능력을 발휘할 가능성이 높습니다.
"""

# =========================
# TOP5 추천
# =========================
def get_top5(user_score):
    scored = []
    for name, traits in job_pool:
        score = job_score(traits, user_score)
        scored.append((name, score))
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
        for name, traits in job_pool:
            scored_jobs.append({
                "name": name,
                "traits": traits,
                "score": job_score(traits, user_score)
            })

        scored_jobs.sort(key=lambda x: x["score"], reverse=True)

        st.session_state.top5 = get_top5(user_score)

        st.session_state.wc = scored_jobs[:16]
        st.session_state.next_wc = []
        st.session_state.wc_i = 0

        st.rerun()

    q = questions[st.session_state.q_i]

    st.progress(st.session_state.q_i / len(questions))
    st.subheader("🎮 스토리로 보는 나의 선택")

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
# 🏆 월드컵
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
    b = wc[i + 1]

    st.progress(i / len(wc))
    st.write("👇 더 끌리는 직업을 선택하세요!")

    col1, col2 = st.columns(2)

    if col1.button(f"🔥 {a['name']}"):
        with st.spinner("분석 중..."):
            time.sleep(0.3)
        st.session_state.next_wc.append(a)
        st.session_state.wc_i += 2
        st.rerun()

    if col2.button(f"🔥 {b['name']}"):
        with st.spinner("분석 중..."):
            time.sleep(0.3)
        st.session_state.next_wc.append(b)
        st.session_state.wc_i += 2
        st.rerun()

# =========================
# 🎯 결과
# =========================
elif st.session_state.stage == "end":

    st.success("🎯 결과 완료!")

    values = [st.session_state.score.get(t, 0) for t in traits]

    fig, ax = plt.subplots()
    ax.bar(traits, values, color="#4f46e5")
    st.pyplot(fig)

    winner = st.session_state.winner

    st.subheader("🏆 최종 직업")
    st.write(winner["name"])

    st.subheader("🏆 TOP 5 추천 직업")

    for name, score in st.session_state.top5:
        st.write(f"⭐ {name} ({score}점)")

    st.subheader("🤖 AI 직업 설명")

    st.markdown(ai_explain(winner["name"], winner["traits"]))

    if st.button("🔄 다시 시작"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
