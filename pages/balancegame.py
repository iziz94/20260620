import streamlit as st
import random
import matplotlib.pyplot as plt

# -----------------------------
# MBTI 매핑
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
# 고양이 매핑
# -----------------------------
cat_map = {
    "solo": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131",
    "team": "https://images.unsplash.com/photo-1552053831-71594a27632d",
    "creative": "https://images.unsplash.com/photo-1543852786-1cf6624b9987",
    "logic": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce",
    "fun": "https://images.unsplash.com/photo-1543852786-1cf6624b9987",
    "stability": "https://images.unsplash.com/photo-1511044568932-338cba0ad803",
}

# -----------------------------
# 직업 데이터 (TOP5)
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
    {"name": "창업가", "tags": ["challenge", "freedom"], "desc": "사업 운영"},
    {"name": "건축가", "tags": ["logic", "creative"], "desc": "건물 설계"},
]

# -----------------------------
# 32강 이상형 월드컵
# -----------------------------
worldcup = [
    {"name": "조용한 연구실", "tag": "solo", "img": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"},
    {"name": "팀 회의", "tag": "team", "img": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f"},
    {"name": "새 기술 도전", "tag": "challenge", "img": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97"},
    {"name": "안정적인 직장", "tag": "stability", "img": "https://images.unsplash.com/photo-1521791136064-7986c2920216"},
    {"name": "예술 작업", "tag": "creative", "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f"},
    {"name": "논리 문제 해결", "tag": "logic", "img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c"},
    {"name": "현장 활동", "tag": "field", "img": "https://images.unsplash.com/photo-1581091870622-1e7a2e1f0b3f"},
    {"name": "컴퓨터 분석", "tag": "tech", "img": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5"},
    {"name": "사람 돕기", "tag": "help", "img": "https://images.unsplash.com/photo-1526256262350-7da7584cf5eb"},
    {"name": "자유로운 삶", "tag": "freedom", "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"},
    {"name": "빠른 결과", "tag": "speed", "img": "https://images.unsplash.com/photo-1508385082359-f38ae991e8f2"},
    {"name": "정확한 결과", "tag": "precision", "img": "https://images.unsplash.com/photo-1523966211575-eb4a01e7dd51"},
    {"name": "돈 중심", "tag": "stability", "img": "https://images.unsplash.com/photo-1554224154-22dec7ec8818"},
    {"name": "재미 중심", "tag": "fun", "img": "https://images.unsplash.com/photo-1520975922284-7c4d3c7c8c63"},
    {"name": "혼자 결정", "tag": "solo", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475"},
    {"name": "팀 결정", "tag": "team", "img": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"},

    # 추가 16개
    {"name": "데이터 분석", "tag": "logic", "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71"},
    {"name": "창의 작업", "tag": "creative", "img": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"},
    {"name": "연구 집중", "tag": "solo", "img": "https://images.unsplash.com/photo-1532094349884-543bc11b234d"},
    {"name": "협업 프로젝트", "tag": "team", "img": "https://images.unsplash.com/photo-1522071820081-009f0129c71c"},
    {"name": "위험한 도전", "tag": "challenge", "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"},
    {"name": "반복 업무", "tag": "stability", "img": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40"},
    {"name": "콘텐츠 제작", "tag": "creative", "img": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97"},
    {"name": "기술 개발", "tag": "tech", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475"},
    {"name": "상담", "tag": "help", "img": "https://images.unsplash.com/photo-1526256262350-7da7584cf5eb"},
    {"name": "자율 업무", "tag": "freedom", "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"},
    {"name": "빠른 판단", "tag": "speed", "img": "https://images.unsplash.com/photo-1508385082359-f38ae991e8f2"},
    {"name": "정밀 작업", "tag": "precision", "img": "https://images.unsplash.com/photo-1523966211575-eb4a01e7dd51"},
    {"name": "창업", "tag": "challenge", "img": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"},
    {"name": "조직 생활", "tag": "stability", "img": "https://images.unsplash.com/photo-1521791136064-7986c2920216"},
    {"name": "혼자 작업", "tag": "solo", "img": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"},
    {"name": "팀 작업", "tag": "team", "img": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f"},
]

# -----------------------------
# Streamlit 설정
# -----------------------------
st.set_page_config(page_title="직업 이상형 월드컵 32강", layout="centered")

st.title("🏆 직업 이상형 월드컵 32강")

if "pool" not in st.session_state:
    st.session_state.pool = random.sample(worldcup, len(worldcup))
    st.session_state.score = {}

# -----------------------------
# MBTI 계산
# -----------------------------
def get_mbti(score):
    best, best_score = None, 0
    for mbti, traits in mbti_map.items():
        match = sum(score.get(t, 0) for t in traits)
        if match > best_score:
            best_score = match
            best = mbti
    return best or "INFP"

# -----------------------------
# TOP 5 직업
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
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -----------------------------
# 고양이
# -----------------------------
def get_top_trait(score):
    return max(score.items(), key=lambda x: x[1])[0] if score else "solo"

# -----------------------------
# 게임 진행
# -----------------------------
pool = st.session_state.pool

if len(pool) > 1:
    a, b = pool[0], pool[1]

    st.subheader("👉 더 끌리는 선택은?")

    col1, col2 = st.columns(2)

    with col1:
        st.image(a["img"], use_container_width=True)
        if st.button(a["name"]):
            st.session_state.score[a["tag"]] = st.session_state.score.get(a["tag"], 0) + 1
            st.session_state.pool = pool[2:]
            st.rerun()

    with col2:
        st.image(b["img"], use_container_width=True)
        if st.button(b["name"]):
            st.session_state.score[b["tag"]] = st.session_state.score.get(b["tag"], 0) + 1
            st.session_state.pool = pool[2:]
            st.rerun()

# -----------------------------
# 결과
# -----------------------------
else:
    st.success("🏆 최종 결과!")

    st.subheader("📊 성향 그래프")
    draw_chart(st.session_state.score)

    mbti = get_mbti(st.session_state.score)
    st.subheader(f"🧠 MBTI 추정: {mbti}")

    st.subheader("🏆 TOP 5 직업")
    for i, job in enumerate(get_jobs(st.session_state.score)):
        st.markdown(f"""
### {i+1}. {job['name']}
- {job['desc']}
- 점수: {job['score']}
        """)

    # 🐱 고양이 결과
    top_trait = get_top_trait(st.session_state.score)
    cat_url = cat_map.get(top_trait)

    st.subheader("🐱 당신의 성향 고양이")

    if cat_url:
        st.image(cat_url, use_container_width=True)
        st.markdown(f"당신은 **{top_trait} 성향 고양이**입니다 🐾")

    if st.button("다시 시작"):
        st.session_state.pool = random.sample(worldcup, len(worldcup))
        st.session_state.score = {}
        st.rerun()
