import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from datetime import datetime

st.set_page_config(
page_title="🌍 Global Earthquake Visualizer",
page_icon="🌍",
layout="wide"
)

st.title("🌍 전세계 지진 시각화")
st.markdown("USGS 실시간 지진 데이터를 활용한 지도 시각화")

# --------------------

# 사이드바

# --------------------

current_year = datetime.now().year

year = st.sidebar.selectbox(
"연도 선택",
list(range(current_year, 1900, -1))
)

min_mag = st.sidebar.slider(
"최소 규모(Magnitude)",
0.0,
10.0,
4.0,
0.1
)

# --------------------

# 데이터 조회 함수

# --------------------

@st.cache_data(ttl=3600)
def load_earthquake_data(year, min_mag):

```
start = f"{year}-01-01"
end = f"{year}-12-31"

url = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query"
    f"?format=geojson"
    f"&starttime={start}"
    f"&endtime={end}"
    f"&minmagnitude={min_mag}"
    f"&limit=20000"
)

response = requests.get(url, timeout=60)
data = response.json()

records = []

for feature in data["features"]:

    coords = feature["geometry"]["coordinates"]

    props = feature["properties"]

    records.append(
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

return pd.DataFrame(records)
```

# --------------------

# 데이터 로딩

# --------------------

with st.spinner("USGS 데이터 불러오는 중..."):

```
df = load_earthquake_data(year, min_mag)
```

if len(df) == 0:
st.warning("조건에 맞는 지진 데이터가 없습니다.")
st.stop()

# --------------------

# 통계

# --------------------

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

# --------------------

# 지도

# --------------------

st.subheader("🗺️ 지진 위치")

layer = pdk.Layer(
"ScatterplotLayer",
data=df,
get_position='[longitude, latitude]',
get_radius='magnitude * 15000',
get_fill_color='[255, 80, 80, 160]',
pickable=True
)

view_state = pdk.ViewState(
latitude=0,
longitude=0,
zoom=1,
pitch=0
)

deck = pdk.Deck(
map_style="mapbox://styles/mapbox/dark-v10",
initial_view_state=view_state,
layers=[layer],
tooltip={
"html": """ <b>위치:</b> {place}<br/> <b>규모:</b> {magnitude}<br/> <b>깊이:</b> {depth} km<br/> <b>시간:</b> {time}
"""
}
)

st.pydeck_chart(deck)

# --------------------

# 테이블

# --------------------

st.subheader("📋 지진 데이터")

st.dataframe(
df.sort_values(
"magnitude",
ascending=False
),
use_container_width=True
)

