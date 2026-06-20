import streamlit as st
import requests

st.title("🐶🐱 펫 사진 뽑기 + 좋아요")

# 상태 초기화
if "pet_url" not in st.session_state:
    st.session_state.pet_url = None
    st.session_state.pet_type = None
    st.session_state.like_count = 0
    st.session_state.liked = False


def get_dog():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    return response.json()["message"]


def get_cat():
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    return response.json()[0]["url"]


# 버튼 영역
col1, col2 = st.columns(2)

with col1:
    if st.button("🐶 강아지 뽑기"):
        st.session_state.pet_url = get_dog()
        st.session_state.pet_type = "🐶 강아지"
        st.session_state.liked = False  # 새 이미지 나오면 좋아요 초기화

with col2:
    if st.button("🐱 고양이 뽑기"):
        st.session_state.pet_url = get_cat()
        st.session_state.pet_type = "🐱 고양이"
        st.session_state.liked = False


# 이미지 출력
if st.session_state.pet_url:
    st.write(f"현재 펫: {st.session_state.pet_type}")
    st.image(st.session_state.pet_url, width=400)

    # 좋아요 버튼
    if st.button("❤️ 좋아요"):
        if not st.session_state.liked:
            st.session_state.like_count += 1
            st.session_state.liked = True
            st.success("좋아요 추가! ❤️")
        else:
            st.warning("이미 좋아요 눌렀어요!")

    st.write(f"❤️ 총 좋아요: {st.session_state.like_count}")
