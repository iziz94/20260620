import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from datetime import datetime

# ----------------------------------

# 페이지 설정

# ----------------------------------

st.set_page_config(
page_title="🌍 Global Earthquake Visualizer",
page_icon="🌍",
layout="wide"
)

st.title("🌍 전세계 지진 시각화")
st.markdown("USGS Earthquake API 기반 실시간 지진 데이터")

# ----------------------------------

# 지역 정의

# ----------------------------------

REGIONS = {
"전세계": None,

```
"아시아": {
    "min_lat": -10,
    "max_lat": 80,
    "min_lon": 25,
    "max_lon": 180
},

"유럽": {
    "min_lat": 35,
    "max_lat": 72,
    "min_lon": -15,
    "max_lon": 45
},

"북아메리카": {
    "min_lat": 5,
    "max_lat": 85,
    "min_lon": -170,
    "max_lon": -50
},

"남아메리카": {
    "min_lat": -60,
    "max_lat": 15,
    "min_lon": -90,
    "max_lon": -30
},

"아프리카": {
    "min_lat": -35,
    "max_lat": 38,
    "min_lon": -20,
    "max_lon": 55
},

"오세아니아": {
    "min_lat": -50,
    "max_lat": 10,
    "min_lon": 110,
    "max_lon": 180
},

"한국": {
    "min_lat": 33,
    "max_lat": 39,
    "min_lon": 124,
    "max_lon": 132
}
```

}

# ----------------------------------

# 사이드바

# ----------------------------------

current_year = datetime.now().year

year = st.sidebar.selectbox(
"📅 연도 선택",
list(range(current_year, 2000, -1))
)

region = st.sidebar.selectbox(
"🌎 지역 선택",
list(REGIONS.keys())
)

min_mag = st.sidebar.slider(
"📈 최소 규모",
1.0,
8.0,
4.0,
0.5
)

if region == "한국" and min_mag < 2.0:
min_mag = 2.0

# ----------------------------------

# 데이터 로딩

# ----------------------------------

@st.cache_data(ttl=3600)
def load_data(year, min_mag):

```
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
            "place": props["place"],
            "time": pd.to_datetime(
                props["time"],
                unit="ms"
            )
        }
    )

return pd.DataFrame(earthquakes)
```

# ----------------------------------

# 데이터 가져오기

# ----------------------------------

with st.spinner("지진 데이터 로딩 중..."):
df = load_data(year, min_mag)

# ----------------------------------

# 지역 필터

# ----------------------------------

if region != "전세계":

```
box = REGIONS[region]

df = df[
    (df["latitude"] >= box["min_lat"]) &
    (df["latitude"] <= box["max_lat"]) &
    (df["longitude"] >= box["min_lon"]) &
    (df["longitude"] <= box["max_lon"])
]
```

if df.empty:
st.warning("해당 조건의 지진 데이터가 없습니다.")
st.stop()

# ----------------------------------

# 통계

# ----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
"지진 수",
f"{len(df):,}"
)

col2.metric(
"최대 규모",
round(df["magnitude"].max(), 1)
)

col3.metric(
"평균 규모",
round(df["magnitude"].mean(), 2)
)

# ----------------------------------

# 지도 중심

# ----------------------------------

center_lat = df["latitude"].mean()
center_lon = df["longitude"].mean()

zoom_levels = {
"전세계": 1,
"아시아": 2,
"유럽": 3,
"북아메리카": 2,
"남아메리카": 2,
"아프리카": 2,
"오세아니아": 2,
"한국": 6
}

view_state = pdk.ViewState(
latitude=center_lat,
longitude=center_lon,
zoom=zoom_levels[region]
)

# ----------------------------------

# 레이어 생성

# ----------------------------------

if region == "한국":

```
earthquake_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["longitude", "latitude"],
    get_radius="magnitude * 50000",
    get_fill_color=[0, 120, 255, 200],
    pickable=True
)

max_mag = df["magnitude"].max()

highlight_df = df[
    df["magnitude"] == max_mag
]

highlight_layer = pdk.Layer(
    "ScatterplotLayer",
    data=highlight_df,
    get_position=["longitude", "latitude"],
    get_radius=150000,
    get_fill_color=[255, 255, 0, 220],
    pickable=True
)

layers = [
    earthquake_layer,
    highlight_layer
]
```

else:

```
earthquake_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["longitude", "latitude"],
    get_radius="magnitude * 15000",
    get_fill_color=[255, 60, 60, 180],
    pickable=True
)

layers = [earthquake_layer]
```

# ----------------------------------

# 지도

# ----------------------------------

deck = pdk.Deck(
initial_view_state=view_state,
layers=layers,
tooltip={
"html": """ <b>위치:</b> {place}<br/> <b>규모:</b> {magnitude}<br/> <b>깊이:</b> {depth} km<br/> <b>시간:</b> {time}
"""
}
)

st.subheader(f"🗺️ {region} 지진 분포")
st.pydeck_chart(deck)

# ----------------------------------

# 한국 전용 정보

# ----------------------------------

if region == "한국":

```
st.subheader("🇰🇷 한국 지진 분석")

latest_df = df.sort_values(
    "time",
    ascending=False
).head(10)

st.info(
    f"최대 규모 지진: M {df['magnitude'].max():.1f}"
)

st.dataframe(
    latest_df[
        [
            "time",
            "magnitude",
            "depth",
            "place"
        ]
    ],
    use_container_width=True
)
```

# ----------------------------------

# 전체 데이터

# ----------------------------------

st.subheader("📋 전체 지진 데이터")

st.dataframe(
df.sort_values(
"magnitude",
ascending=False
),
use_container_width=True
)
