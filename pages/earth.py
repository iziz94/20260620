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
st.markdown("USGS Earthquake API 기반 지진 데이터 시각화")

# -----------------------------
# 지역 설정
# -----------------------------
REGIONS = {
    "전세계": None,
    "아시아": {"min_lat": -10, "max_lat": 80, "min_lon": 25, "max_lon": 180},
    "유럽": {"min_lat": 35, "max_lat": 72, "min_lon": -15, "max_lon": 45},
    "북아메리카": {"min_lat": 5, "max_lat": 85, "min_lon": -170, "max_lon": -50},
    "남아메리카": {"min_lat": -60, "max_lat": 15, "min_lon": -90, "max_lon": -30},
    "아프리카": {"min_lat": -35, "max_lat": 38, "min_lon": -20, "max_lon": 55},
    "오세아니아": {"min_lat": -50, "max_lat": 10, "min_lon": 110, "max_lon": 180},
    "한국": {"min_lat": 33, "max_lat": 39, "min_lon": 124, "max_lon": 132},
}

# -----------------------------
# 사이드바
# -----------------------------
current_year = datetime.now().year

year = st.sidebar.selectbox(
    "📅 연도 선택",
    list(range(current_year, 2000, -1))
)

region = st.sidebar.selectbox(
    "🌍 지역 선택",
    list(REGIONS.keys())
)

min_mag = st.sidebar.slider(
    "📈 최소 규모",
    1.0, 8.0, 4.0, 0.5
)

# 한국은 최소 규모 보정
if region == "한국" and min_mag < 2.0:
    min_mag = 2.0

# -----------------------------
# 데이터 로딩
# -----------------------------
@st.cache_data(ttl=3600)
def load_data(year, min_mag):

    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        f"?format=geojson"
        f"&starttime={year}-01-01"
        f"&endtime={year}-12-31"
        f"&minmagnitude={min_mag}"
        f"&limit=5000"
    )

    try:
        r = requests.get(url, timeout=60)
        data = r.json()
    except:
        return pd.DataFrame()

    rows = []

    for f in data.get("features", []):
        coords = f["geometry"]["coordinates"]
        props = f["properties"]

        rows.append({
            "longitude": coords[0],
            "latitude": coords[1],
            "depth": coords[2],
            "magnitude": props["mag"],
            "place": props["place"],
            "time": pd.to_datetime(props["time"], unit="ms")
        })

    return pd.DataFrame(rows)

# -----------------------------
# 데이터 가져오기
# -----------------------------
with st.spinner("지진 데이터 불러오는 중..."):
    df = load_data(year, min_mag)

if df.empty:
    st.warning("데이터가 없습니다.")
    st.stop()

# -----------------------------
# 지역 필터
# -----------------------------
if region != "전세계":
    box = REGIONS[region]
    df = df[
        (df["latitude"] >= box["min_lat"]) &
        (df["latitude"] <= box["max_lat"]) &
        (df["longitude"] >= box["min_lon"]) &
        (df["longitude"] <= box["max_lon"])
    ]

if df.empty:
    st.warning("해당 지역 데이터가 없습니다.")
    st.stop()

# -----------------------------
# 통계
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("지진 수", f"{len(df):,}")
col2.metric("최대 규모", f"{df['magnitude'].max():.1f}")
col3.metric("평균 규모", f"{df['magnitude'].mean():.2f}")

# -----------------------------
# 지도 중심
# -----------------------------
center_lat = df["latitude"].mean()
center_lon = df["longitude"].mean()

zoom_map = {
    "전세계": 1,
    "아시아": 2,
    "유럽": 3,
    "북아메리카": 2,
    "남아메리카": 2,
    "아프리카": 2,
    "오세아니아": 2,
    "한국": 6
}

# -----------------------------
# 한국 강조
# -----------------------------
if region == "한국":
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_radius="magnitude * 50000",
        get_fill_color=[0, 120, 255, 200],
        pickable=True
    )

    max_mag = df["magnitude"].max()
    highlight = df[df["magnitude"] == max_mag]

    highlight_layer = pdk.Layer(
        "ScatterplotLayer",
        data=highlight,
        get_position=["longitude", "latitude"],
        get_radius=150000,
        get_fill_color=[255, 255, 0, 255],
        pickable=True
    )

    layers = [layer, highlight_layer]

else:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_radius="magnitude * 15000",
        get_fill_color=[255, 60, 60, 160],
        pickable=True
    )

    layers = [layer]

# -----------------------------
# 지도
# -----------------------------
deck = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=zoom_map[region]
    ),
    layers=layers,
    tooltip={
        "html": """
        <b>장소:</b> {place}<br/>
        <b>규모:</b> {magnitude}<br/>
        <b>깊이:</b> {depth} km<br/>
        <b>시간:</b> {time}
        """
    }
)

st.subheader("🗺️ 지진 지도")
st.pydeck_chart(deck)

# -----------------------------
# 한국 분석
# -----------------------------
if region == "한국":

    st.subheader("🇰🇷 한국 지진 분석")

    st.write(f"최대 규모: M {df['magnitude'].max():.1f}")

    st.dataframe(
        df.sort_values("time", ascending=False).head(10),
        use_container_width=True
    )

# -----------------------------
# 전체 데이터
# -----------------------------
st.subheader("📋 데이터")

st.dataframe(
    df.sort_values("magnitude", ascending=False),
    use_container_width=True
)
