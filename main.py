import streamlit as st
import pandas as pd

st.set_page_config(page_title="버스 정보 시스템", page_icon="🚌")

# 1. 데이터 로드
df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})
stops = sorted(list(set([stop.strip() for route in df['route'].dropna() for stop in route.split('-')])))
FARE_MAP = {'어린이': 550, '청소년': 900, '성인': 1500}

# 2. 상태 관리 (관리자 모드 + 잠금 모드)
if 'admin' not in st.session_state: st.session_state.admin = False
if 'locked' not in st.session_state: st.session_state.locked = False # 배포 종료 여부

with st.sidebar:
    st.header("⚙️ 관리자 설정")
    pw = st.text_input("관리자 코드", type="password")
    if st.button("인증/로그아웃"):
        if pw == "3934":
            st.session_state.admin = not st.session_state.admin
            st.rerun()

    if st.session_state.admin:
        st.markdown("---")
        st.warning("⚠️ 운영자 제어 모드")
        # 배포 종료/재개 버튼 (서버를 끄지 않고 잠금/해제만 함)
        if not st.session_state.locked:
            if st.button("🚫 무료 배포 종료 (잠금)"):
                st.session_state.locked = True
                st.rerun()
        else:
            if st.button("✅ 무료 배포 재개 (해제)"):
                st.session_state.locked = False
                st.rerun()

# 3. 메인 화면 제어 (잠금 모드일 때 접속 차단)
if st.session_state.locked and not st.session_state.admin:
    st.title("🚧 서비스 종료")
    st.info("무료 배포 기간이 종료되었습니다. 이용해주셔서 감사합니다.")
    st.stop() # 여기서 멈춤

st.title("🚌 통합 버스 정산 시스템")
# ... (이하 조회 로직은 동일) ...
passenger_type = st.radio("요금 계산 기준:", ('어린이', '청소년', '성인'), index=2, horizontal=True)
col1, col2, col3 = st.columns(3)
with col1: start_point = st.selectbox("출발지", ["선택하세요"] + stops)
with col2: end_point = st.selectbox("도착지", ["선택하세요"] + stops)
with col3: bus_no = st.text_input("버스 번호", value="402")

if st.button("조회"):
    query = df
    if bus_no: query = query[query['bus_no'] == bus_no]
    if start_point != "선택하세요": query = query[query['route'].str.contains(start_point)]
    if end_point != "선택하세요": query = query[query['route'].str.contains(end_point)]
    if not query.empty:
        for _, d in query.iterrows():
            st.success(f"🚌 {d['bus_no']}번 버스 정보")
            st.markdown(f"**경로:** {d['route']}")
            st.caption(f"💰 {passenger_type} 요금: {FARE_MAP[passenger_type]:,}원")
            st.markdown("---")
    else: st.warning("정보 없음")

st.markdown("---")
st.markdown("<div style='color: gray;'>🔍 @devjin_747 | 📩 kyjin0808@naver.com</div>", unsafe_allow_html=True)
