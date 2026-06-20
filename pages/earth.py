import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from datetime import datetime

st.set_page_config(
    page_title="Global Earthquake Visualizer",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 전세계 지진 시각화")

current_year = datetime.now().year

year = st.sidebar.selectbox(
    "연도 선택",
    list(range(current_year, 2000, -1))
)

min_mag = st.sidebar.slider(
    "최소 규모",
    1.0,
    8.0,
    4.0,
    0.5
)


@st.cache_data(ttl=3600)
def load_data(year, min_mag):

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        f"?format=geojson"
        f"&starttime={start_date}"
        f"&endtime={end_date}"
        f"&minmagnitude={min_mag}"
        f"&limit=5000"
    )

    response = requests.get(url, timeout=60)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()

    earthquakes = []

    for feature in data["features"]:

        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]

        earthquakes.append(
            {
                "longitude": coords[0],
                "latitude": coords[1],
                "depth": coords[2],
                "magnitude": props["mag"],
                "place": props["place"]
            }
        )

    return pd.DataFrame(earthquakes)


with st.spinner("지진 데이터 불러오는 중..."):
    df = load_data(year, min_mag)

if df.empty:
    st.warning("데이터가 없습니다.")
    st.stop()

col1, col2, col3 = st.columns(3)

col1.metric("지진 수", f"{len(df):,}")
col2.metric("최대 규모", round(df["magnitude"].max(), 1))
col3.metric("평균 규모", round(df["magnitude"].mean(), 2))

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["longitude", "latitude"],
    get_radius="magnitude * 15000",
    get_fill_color=[255, 0, 0, 140],
    pickable=True
)

view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1
)

deck = pdk.Deck(
    initial_view_state=view_state,
    layers=[layer],
    tooltip={
        "html": """
        <b>위치:</b> {place}<br/>
        <b>규모:</b> {magnitude}<br/>
        <b>깊이:</b> {depth} km
        """
    }
)

st.pydeck_chart(deck)

st.subheader("지진 데이터")

st.dataframe(
    df.sort_values(
        "magnitude",
        ascending=False
    ),
    use_container_width=True
)
