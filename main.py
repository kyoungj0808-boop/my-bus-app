import streamlit as st
import pandas as pd

st.set_page_config(page_title="버스 정산 시스템", page_icon="🚌")

# 1. 데이터 로드
try:
    df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})
except:
    df = pd.DataFrame(columns=['bus_no', 'route', 'info'])

FARE_MAP = {'어린이': 550, '청소년': 900, '성인': 1500}

# 2. 관리자 및 잠금 상태
if 'admin' not in st.session_state: st.session_state.admin = False
if 'locked' not in st.session_state: st.session_state.locked = False

with st.sidebar:
    st.header("⚙️ 관리자 설정")
    pw = st.text_input("코드", type="password")
    if st.button("인증"):
        if pw == "3934": st.session_state.admin = True; st.rerun()
    
    if st.session_state.admin:
        if st.button("🚫 배포 종료(잠금)"): st.session_state.locked = True; st.rerun()
        if st.button("✅ 배포 재개(해제)"): st.session_state.locked = False; st.rerun()

# 3. 서비스 잠금 시 차단
if st.session_state.locked and not st.session_state.admin:
    st.title("🚧 서비스 점검 중")
    st.stop()

# 4. 인스타 감성 UI 및 기능
st.title("🚌 통합 버스 정산 시스템")
passenger_type = st.radio("요금 기준:", ('어린이', '청소년', '성인'), index=2, horizontal=True)
bus_no = st.text_input("버스 번호", value="402")

if st.button("조회"):
    result = df[df['bus_no'] == bus_no.strip()]
    if not result.empty:
        for _, row in result.iterrows():
            st.success(f"🚌 {row['bus_no']}번 버스 정보")
            st.markdown(f"**경로:** {row['route']}")
            st.caption(f"💰 {passenger_type} 요금: {FARE_MAP[passenger_type]:,}원")
            st.caption(f"상세: {row['info']}")
            st.markdown("---")
    else:
        st.warning("등록된 노선을 찾을 수 없습니다.")

st.markdown("🔍 @devjin_747 | 📩 kyjin0808@naver.com")
