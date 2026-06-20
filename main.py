import streamlit as st
import requests

st.set_page_config(
    page_title="랜덤 반려동물 사진",
    page_icon="🐾"
)

st.title("🐾 랜덤 반려동물 사진 뽑기")

animal = st.selectbox(
    "동물을 선택하세요",
    ["강아지", "고양이"]
)

if st.button("사진 뽑기"):
    with st.spinner("사진을 가져오는 중..."):

        if animal == "강아지":
            # 강아지 API 호출
            response = requests.get(
                "https://dog.ceo/api/breeds/image/random"
            )

            if response.status_code == 200:
                data = response.json()

                image_url = data["message"]

                # URL에서 품종 추출
                breed = image_url.split("/")[4]

                st.image(
                    image_url,
                    caption=f"🐶 품종: {breed}",
                    use_container_width=True
                )

                st.success(f"품종 정보: {breed}")

            else:
                st.error("강아지 사진을 불러오지 못했습니다.")

        else:
            # 고양이 API 호출
            response = requests.get(
                "https://api.thecatapi.com/v1/images/search"
            )

            if response.status_code == 200:
                data = response.json()

                image_url = data[0]["url"]

                st.image(
                    image_url,
                    caption="🐱 랜덤 고양이",
                    use_container_width=True
                )

                # 품종 정보 확인
                breeds = data[0].get("breeds", [])

                if breeds:
                    breed_name = breeds[0]["name"]

                    st.success(f"품종 정보: {breed_name}")

                    st.write("### 상세 정보")
                    st.write(
                        f"**원산지:** {breeds[0].get('origin', '정보 없음')}"
                    )
                    st.write(
                        f"**성격:** {breeds[0].get('temperament', '정보 없음')}"
                    )

                else:
                    st.info("품종 정보가 제공되지 않는 사진입니다.")

            else:
                st.error("고양이 사진을 불러오지 못했습니다.")
