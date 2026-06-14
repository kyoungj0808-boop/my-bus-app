import streamlit as st
import pandas as pd

st.set_page_config(page_title="버스 정보 시스템", page_icon="🚌")

# 1. 데이터 로드 및 전처리
df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})

# 자동완성을 위한 지점 목록 추출 (route가 '우이동-중앙대' 형태라고 가정)
locations = set()
for route in df['route'].dropna():
    parts = route.split('-')
    for p in parts: locations.add(p.strip())
locations = sorted(list(locations))

FARE_MAP = {'어린이': 550, '청소년': 900, '성인': 1500}

st.title("🚌 통합 버스 정산 시스템")

# 승객 유형 설정
passenger_type = st.radio("요금 계산 기준:", ('어린이', '청소년', '성인'), index=2, horizontal=True)

# 2. 자동완성 입력창
col1, col2, col3 = st.columns(3)
with col1:
    start_point = st.selectbox("출발지", ["선택하세요"] + locations)
with col2:
    end_point = st.selectbox("도착지", ["선택하세요"] + locations)
with col3:
    bus_no = st.text_input("버스 번호")

if st.button("조회"):
    # 버스 번호와 출발/도착지가 모두 맞는 데이터 필터링
    query = df
    if bus_no: query = query[query['bus_no'] == bus_no]
    if start_point != "선택하세요": query = query[query['route'].str.contains(start_point)]
    if end_point != "선택하세요": query = query[query['route'].str.contains(end_point)]
    
    if not query.empty:
        d = query.iloc[0]
        st.success(f"🚌 {d['bus_no']}번 버스 정보")
        st.markdown(f"**경로:** {d['route']}")
        st.caption(f"상세 정보: {d['info']}")
        st.caption(f"💰 {passenger_type} 요금: {FARE_MAP[passenger_type]:,}원")
    else:
        st.warning("해당 조건의 버스를 찾을 수 없습니다.")
