import streamlit as st
import pandas as pd

st.set_page_config(page_title="버스 정보 시스템", page_icon="🚌")

# 1. 데이터 로드
df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})

# 402번 노선 데이터만 추출하여 정류장 목록 생성
# 정류장 데이터가 '장지동-시청역' 처럼 되어 있다면, 
# 실제 40개의 정류장 리스트를 CSV에 추가하면 그대로 반영됩니다.
# 우선 현재 route 데이터를 기준으로 정류장 목록을 만듭니다.
stops = set()
for route in df['route'].dropna():
    for stop in route.split('-'):
        stops.add(stop.strip())
stops = sorted(list(stops))

FARE_MAP = {'어린이': 550, '청소년': 900, '성인': 1500}

# 2. 관리자 설정
if 'admin' not in st.session_state: st.session_state.admin = False
with st.sidebar:
    st.header("⚙️ 관리자 설정")
    pw = st.text_input("관리자 코드", type="password")
    if st.button("인증/로그아웃"):
        if pw == "3934":
            st.session_state.admin = not st.session_state.admin
            st.rerun()

st.title("🚌 통합 버스 정산 시스템")
passenger_type = st.radio("요금 계산 기준:", ('어린이', '청소년', '성인'), index=2, horizontal=True)

# 3. 출발/도착지 및 버스 번호 조회
col1, col2, col3 = st.columns(3)
with col1: start_point = st.selectbox("출발지", ["선택하세요"] + stops)
with col2: end_point = st.selectbox("도착지", ["선택하세요"] + stops)
with col3: bus_no = st.text_input("버스 번호", value="402") # 기본값을 402로 고정

if st.button("조회"):
    query = df
    if bus_no: query = query[query['bus_no'] == bus_no]
    if start_point != "선택하세요": query = query[query['route'].str.contains(start_point)]
    if end_point != "선택하세요": query = query[query['route'].str.contains(end_point)]
    
    if not query.empty:
        for _, d in query.iterrows():
            st.success(f"🚌 {d['bus_no']}번 버스 정보")
            st.markdown(f"**경로:** {d['route']}")
            st.caption(f"상세 정보: {d['info']}")
            st.caption(f"💰 {passenger_type} 요금: {FARE_MAP[passenger_type]:,}원")
            st.markdown("---")
    else:
        st.warning("등록된 노선 정보를 찾을 수 없습니다.")

# 4. 제작자 정보 복구
st.markdown("### 제작 과정 및 문의")
st.markdown("<div style='color: gray;'>🔍 @devjin_747 | 📩 kyjin0808@naver.com</div>", unsafe_allow_html=True)
