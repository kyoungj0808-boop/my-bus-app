import streamlit as st
import hashlib
import os
import pandas as pd

# [보안 설정]
SECRET_KEY = os.getenv("APP_SECRET_KEY", "BOOP_SYSTEM_747")
ADMIN_CODE = os.getenv("ADMIN_MASTER_CODE", "3934")

# [버스 정보 조회 함수: CSV 데이터 기반]
def get_bus_info(bus_num):
    if not os.path.exists("bus_data.csv"):
        return None
    try:
        df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})
        result = df[df['bus_no'] == bus_num]
        if not result.empty:
            return result.iloc[0]
    except Exception:
        return None
    return None

# [기사님 전용 대시보드]
def show_driver_dashboard():
    st.success("데이터 접근 승인 완료: 운행 모드 가동")
    
    # 2. 입력창에서 ':' 제거
    bus_number = st.text_input("버스 번호 입력 (예: 503)")
    
    if bus_number:
        data = get_bus_info(bus_number)
        if data is not None:
            # 3. 지정된 양식으로 출력 (적출 데이터 기반)
            st.info(f"🚌 {bus_number}번 버스 노선 정보")
            st.write(f"첫차시간: {data['first']}")
            st.write(f"막차시간: {data['last']}")
            st.write(f"{data['route']}{data['info']}")
        else:
            st.warning("등록되지 않은 노선번호입니다.")

    st.markdown("---")
    if st.button("정산 전송"):
        st.balloons()
        st.write("✅ 정산 데이터가 서버에 기록되었습니다.")
    
    # 1. "로그아웃" 버튼을 "메인화면"으로 변경
    if st.button("메인화면"):
        st.session_state['bus_auth'] = False
        st.session_state['system_mode'] = 'HOME'
        st.rerun()

# [전역 초기화]
st.set_page_config(page_title="통합 버스 정산 시스템", page_icon="🚌")
if 'admin_active' not in st.session_state: st.session_state['admin_active'] = False
if 'system_mode' not in st.session_state: st.session_state['system_mode'] = 'HOME'
if 'bus_auth' not in st.session_state: st.session_state['bus_auth'] = False

# [관리자 모드]
with st.sidebar:
    st.title("⚙️ 관리자 서버")
    admin_password = st.text_input("마스터 코드", type="password")
    if st.button("인증"):
        if admin_password == ADMIN_CODE:
            st.session_state['admin_active'] = True
            st.rerun()

# [메인 로직]
SYSTEM_MODE = st.session_state['system_mode']

if SYSTEM_MODE == 'HOME':
    st.title("🚌 통합 버스 정산 시스템")
    if st.button("서울 기사님 모드 입장"):
        st.session_state['system_mode'] = 'SEOUL'
        st.rerun()

elif SYSTEM_MODE == 'SEOUL':
    if not st.session_state['bus_auth']:
        st.title("🚌 서울 기사님 전용 테스트")
        password = st.text_input("인증키 입력", type="password")
        if st.button("인증 확인"):
            if password == "1234":
                st.session_state['bus_auth'] = True
                st.rerun()
    else:
        show_driver_dashboard()

st.markdown("---")
st.markdown("<div style='color: gray; font-size: 0.95em;'>🔍 @devjin_747 | 📩 kyjin0808@naver.com</div>", unsafe_allow_html=True)
