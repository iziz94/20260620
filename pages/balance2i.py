import streamlit as st
import matplotlib.pyplot as plt
import random
import time
import math

# =========================
# 기본 설정
# =========================

st.set_page_config(
    page_title="진로 월드컵",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 미래 직업 찾기 게임")
st.caption("중학생을 위한 스토리형 진로 탐색")

# =========================
# 상태 초기화
# =========================

if "stage" not in st.session_state:
    st.session_state.stage = "quiz"

if "q_i" not in st.session_state:
    st.session_state.q_i = 0

if "score" not in st.session_state:
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
    "creative",
    "logic",
    "team",
    "solo",
    "challenge",
    "stability",
    "help",
    "speed",
    "freedom"
]

# =========================
# 중학생 스토리 질문
# =========================

questions = [

(
"🎡 친구들과 놀이공원에 갔다!",
"지도를 보며 계획 세우기",
"재밌어 보이는 곳부터 가기",
"logic",
"freedom"
),

(
"🎮 게임에서 더 재밌는 건?",
"혼자 랭크 올리기",
"친구들과 팀플하기",
"solo",
"team"
),

(
"🎁 친구 생일 선물",
"직접 만들어 준다",
"실용적인 걸 사준다",
"creative",
"logic"
),

(
"🏫 학교 축제 준비",
"아이디어 내기",
"실행하기",
"creative",
"speed"
),

(
"📚 수행평가 시작",
"계획표 먼저 만들기",
"바로 시작하기",
"stability",
"challenge"
),

(
"🚀 새로운 동아리",
"일단 들어가 본다",
"후기부터 찾아본다",
"challenge",
"logic"
),

(
"🎬 영화 볼 때",
"결말 추리하기",
"감정 이입하기",
"logic",
"help"
),

(
"🏕️ 수련회",
"새 친구 만들기",
"친한 친구랑 다니기",
"team",
"solo"
),

(
"🧩 어려운 문제",
"끝까지 혼자 해결",
"친구에게 도움 요청",
"solo",
"team"
),

(
"📱 단톡방",
"정리해서 결론 내기",
"분위기 맞추기",
"logic",
"help"
),

(
"⚽ 체육대회",
"주장 맡기",
"응원하기",
"challenge",
"team"
),

(
"🎨 자유 과제",
"내 스타일대로",
"선생님 예시 참고",
"creative",
"stability"
),

(
"🚴 여행 간다면",
"모험 여행",
"안전 여행",
"challenge",
"stability"
),

(
"🎤 발표 시간",
"앞에 나가 발표",
"자료 정리 담당",
"challenge",
"solo"
),

(
"🎮 게임 캐릭터",
"마법사",
"전사",
"creative",
"speed"
),

(
"🏠 주말",
"집에서 취미",
"밖에서 활동",
"solo",
"team"
),

(
"📖 책 고르기",
"소설",
"과학책",
"creative",
"logic"
),

(
"🐶 길 잃은 강아지 발견",
"직접 도와준다",
"주변 어른 부른다",
"help",
"logic"
),

(
"💡 아이디어가 떠오르면",
"바로 실행",
"계획 세우기",
"speed",
"stability"
),

(
"🌍 미래 목표",
"내가 좋아하는 일",
"안정적인 직업",
"freedom",
"stability"
)

]

# =========================
# 직업 데이터
# =========================

job_pool = {

"게임 개발자":{
"traits":["creative","logic"],
"salary":"4500만원",
"difficulty":"★★★★☆",
"desc":"게임을 만드는 직업"
},

"AI 연구원":{
"traits":["logic","creative"],
"salary":"7000만원",
"difficulty":"★★★★★",
"desc":"인공지능 기술 연구"
},

"의사":{
"traits":["logic","help"],
"salary":"1억~2억원",
"difficulty":"★★★★★",
"desc":"환자를 치료"
},

"교사":{
"traits":["help","team"],
"salary":"4000~7000만원",
"difficulty":"★★★☆☆",
"desc":"학생 교육"
},

"심리상담사":{
"traits":["help","team"],
"salary":"3500~6000만원",
"difficulty":"★★★★☆",
"desc":"상담 및 심리 지원"
},

"변호사":{
"traits":["logic","challenge"],
"salary":"8000만원 이상",
"difficulty":"★★★★★",
"desc":"법률 전문가"
},

"경찰관":{
"traits":["challenge","help"],
"salary":"4000~7000만원",
"difficulty":"★★★★☆",
"desc":"치안 유지"
},

"소방관":{
"traits":["challenge","help"],
"salary":"4000~7000만원",
"difficulty":"★★★★☆",
"desc":"재난 구조"
},

"유튜버":{
"traits":["creative","freedom"],
"salary":"개인차 매우 큼",
"difficulty":"★★★☆☆",
"desc":"영상 콘텐츠 제작"
},

"PD":{
"traits":["creative","team"],
"salary":"5000만원",
"difficulty":"★★★★☆",
"desc":"방송 제작 총괄"
},

"기자":{
"traits":["challenge","team"],
"salary":"4500만원",
"difficulty":"★★★★☆",
"desc":"뉴스 취재"
},

"아나운서":{
"traits":["team","challenge"],
"salary":"5000만원",
"difficulty":"★★★★☆",
"desc":"방송 진행"
},

"UX 디자이너":{
"traits":["creative","team"],
"salary":"4500만원",
"difficulty":"★★★☆☆",
"desc":"사용자 경험 설계"
},

"그래픽 디자이너":{
"traits":["creative"],
"salary":"3500만원",
"difficulty":"★★★☆☆",
"desc":"시각 디자인"
},

"일러스트레이터":{
"traits":["creative","solo"],
"salary":"개인차 큼",
"difficulty":"★★★☆☆",
"desc":"그림 제작"
},

"로봇공학자":{
"traits":["logic","creative"],
"salary":"7000만원",
"difficulty":"★★★★★",
"desc":"로봇 개발"
}

}
# =========================
# 직업 적합도 계산
# =========================

def get_job_score(user_score, job_traits):

    score = 0

    for t in job_traits:
        score += user_score.get(t, 0)

    return score


# =========================
# TOP5 추천
# =========================

def get_top_jobs(user_score):

    result = []

    for job, data in job_pool.items():

        score = get_job_score(
            user_score,
            data["traits"]
        )

        result.append(
            (job, score)
        )

    result.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return result[:5]


# =========================
# AI 리포트
# =========================

def ai_report(job):

    data = job_pool[job]

    return f"""
### 🤖 AI 진로 리포트

🏆 추천 직업
**{job}**

💡 하는 일

{data['desc']}

💰 평균 연봉

{data['salary']}

📚 준비 난이도

{data['difficulty']}

🚀 추천 이유

당신의 성향이
{", ".join(data['traits'])}
과 높은 관련성을 보입니다.

해당 분야에서 강점을 발휘할 가능성이 높습니다.
"""


# =========================
# 레이더 차트
# =========================

def draw_radar(score_dict):

    labels = traits

    values = [
        score_dict.get(t, 0)
        for t in labels
    ]

    values += values[:1]

    angles = [
        n / float(len(labels))
        * 2
        * math.pi
        for n in range(len(labels))
    ]

    angles += angles[:1]

    fig = plt.figure(figsize=(6,6))

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(labels)

    st.pyplot(fig)


# =========================
# QUIZ
# =========================

if st.session_state.stage == "quiz":

    if st.session_state.q_i >= len(questions):

        user_score = st.session_state.score

        ranked_jobs = []

        for job, data in job_pool.items():

            ranked_jobs.append({

                "name": job,

                "traits": data["traits"],

                "score":
                get_job_score(
                    user_score,
                    data["traits"]
                )
            })

        ranked_jobs.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        st.session_state.top5 = get_top_jobs(
            user_score
        )

        wc_jobs = ranked_jobs[:16]

        random.shuffle(wc_jobs)

        st.session_state.wc = wc_jobs
        st.session_state.next_wc = []
        st.session_state.wc_i = 0

        st.session_state.stage = "worldcup"

        st.rerun()

    q = questions[
        st.session_state.q_i
    ]

    st.progress(
        (st.session_state.q_i+1)
        / len(questions)
    )

    st.subheader(
        f"문제 {st.session_state.q_i+1}"
    )

    st.write(q[0])

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            f"🅰️ {q[1]}",
            use_container_width=True
        ):

            st.session_state.score[q[3]] = \
                st.session_state.score.get(
                    q[3],
                    0
                ) + 1

            st.session_state.q_i += 1

            st.rerun()

    with col2:

        if st.button(
            f"🅱️ {q[2]}",
            use_container_width=True
        ):

            st.session_state.score[q[4]] = \
                st.session_state.score.get(
                    q[4],
                    0
                ) + 1

            st.session_state.q_i += 1

            st.rerun()


# =========================
# 월드컵
# =========================

elif st.session_state.stage == "worldcup":

    wc = st.session_state.wc

    if len(wc) == 1:

        st.session_state.winner = wc[0]

        st.session_state.stage = "result"

        st.rerun()

    i = st.session_state.wc_i

    if i >= len(wc) - 1:

        st.session_state.wc = \
            st.session_state.next_wc

        st.session_state.next_wc = []

        st.session_state.wc_i = 0

        st.rerun()

    a = wc[i]
    b = wc[i+1]

    round_name = {
        16:"16강",
        8:"8강",
        4:"4강",
        2:"결승"
    }

    st.subheader(
        f"⚔️ 직업 월드컵 {round_name.get(len(wc),'')}"
    )

    st.write(
        "더 끌리는 직업을 선택하세요!"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            a["name"],
            use_container_width=True
        ):

            st.session_state.next_wc.append(a)

            st.session_state.wc_i += 2

            st.rerun()

    with col2:

        if st.button(
            b["name"],
            use_container_width=True
        ):

            st.session_state.next_wc.append(b)

            st.session_state.wc_i += 2

            st.rerun()


# =========================
# 결과
# =========================

elif st.session_state.stage == "result":

    winner = st.session_state.winner

    st.success(
        "🎉 진로 탐색 완료!"
    )

    st.subheader(
        "📊 나의 성향 분석"
    )

    draw_radar(
        st.session_state.score
    )

    st.divider()

    st.subheader(
        "🏆 추천 직업 TOP5"
    )

    for job, score in \
        st.session_state.top5:

        percent = min(
            100,
            50 + score*10
        )

        st.write(
            f"⭐ {job}"
        )

        st.progress(
            percent/100
        )

        st.write(
            f"적합도 {percent}%"
        )

    st.divider()

    st.subheader(
        "🥇 최종 우승 직업"
    )

    st.markdown(
        f"# {winner['name']}"
    )

    st.image(
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
        use_container_width=True
    )

    st.divider()

    st.markdown(
        ai_report(
            winner["name"]
        )
    )

    st.divider()

    st.subheader(
        "🌟 한 줄 조언"
    )

    advice = [
        "관심 있는 분야를 직접 체험해보세요.",
        "진로는 한 번에 결정되지 않아도 괜찮아요.",
        "좋아하는 것과 잘하는 것을 함께 찾아보세요.",
        "지금의 선택이 미래를 만드는 첫걸음입니다."
    ]

    st.info(
        random.choice(advice)
    )

    if st.button(
        "🔄 처음부터 다시 하기"
    ):

        for k in list(
            st.session_state.keys()
        ):
            del st.session_state[k]

        st.rerun()
