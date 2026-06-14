import streamlit as st
import os
import pandas as pd

# [전역 초기화]
st.set_page_config(page_title="통합 버스 정산 시스템", page_icon="🚌")

if 'bus_auth' not in st.session_state: st.session_state['bus_auth'] = False
if 'system_mode' not in st.session_state: st.session_state['system_mode'] = 'HOME'

# [버스 정보 조회 함수]
def get_bus_info(bus_num):
    if not os.path.exists("bus_data.csv"): return None
    try:
        df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})
        result = df[df['bus_no'] == bus_num]
        return result.iloc[0] if not result.empty else None
    except: return None

# [대시보드 함수]
def show_dashboard():
    st.success("운행 모드 가동 중")
    bus_number = st.text_input("버스 번호 입력 (예: 503)")
    if bus_number:
        data = get_bus_info(bus_number)
        if data is not None:
            st.info(f"🚌 {bus_number}번 버스 노선 정보")
            st.write(f"첫차시간: {data['first']}")
            st.write(f"막차시간: {data['last']}")
            st.write(f"{data['route']}{data['info']}")
        else:
            st.warning("등록되지 않은 노선번호입니다.")
    
    st.markdown("---")
    if st.button("메인화면"):
        st.session_state['bus_auth'] = False
        st.session_state['system_mode'] = 'HOME'
        st.rerun()

# [메인 제어 로직]
if st.session_state['system_mode'] == 'HOME':
    st.title("🚌 통합 버스 정산 시스템")
    if st.button("서울 기사님 모드 입장"):
        st.session_state['system_mode'] = 'SEOUL'
        st.rerun()
else:
    if not st.session_state['bus_auth']:
        st.title("🚌 인증 필요")
        pwd = st.text_input("인증키", type="password")
        if st.button("인증 확인"):
            if pwd == "1234":
                st.session_state['bus_auth'] = True
                st.rerun()
    else:
        show_dashboard()
