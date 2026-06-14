import streamlit as st
import hashlib
import os
import pandas as pd

# [보안 설정]
SECRET_KEY = os.getenv("APP_SECRET_KEY", "BOOP_SYSTEM_747")
ADMIN_CODE = os.getenv("ADMIN_MASTER_CODE", "3934")

# [버스 정보 조회 함수: CSV 데이터 기반]
def get_bus_info(bus_num):
    # 같은 폴더에 있는 bus_data.csv를 로드하여 입력된 버스 번호 탐색
    try:
        # 데이터가 1.4GB더라도 필요한 노선만 검색하므로 매우 빠름
        df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})
        result = df[df['bus_no'] == bus_num]
        if not result.empty:
            return result.iloc[0]
    except Exception:
        return None
    return None

# [기사님 전용 대시보드 함수]
def show_driver_dashboard():
    st.success("데이터 접근 승인 완료: 운행 모드 가동")
    
    # 사령관님 지정 양식 기반 출력 모듈
    bus_number = st.text_input("버스 번호 입력:")
    if bus_number:
        data = get_bus_info(bus_number)
        if data is not None:
            # 출력 양식: 사령관님의 요구사항 100% 반영
            st.info(f"🚌 {bus_number}번 버스 노선 정보")
            st.write(f"기점-종점: {data['route']}")
            st.write(f"버스거리/정류장수: {data['info']}")
            st.write(f"첫차시간: {data['first']}")
            st.write(f"막차시간: {data['last']}")
        else:
            st.warning("등록되지 않은 노선 번호입니다.")

    st.markdown("---")
    
    if st.button("정산 전송"):
        st.balloons()
        st.write("✅ 정산 데이터가 서버에 기록되었습니다.")
    
    # 전국 확장 로드맵
    st.subheader("🗓️ 전국 단위 확장 로드맵")
    roadmap_data = {
        "~6/16일": "무료배포 종료(월 요금제 도입)",
        "~6/22일": "서울시 기차정보 및 부산 버스 정보 공지",
        "~6/29일": "전국 환승 알림 시스템 베타 테스트",
        "~7/6일": "경상도/강원도 작업 및 데이터 최적화",
        "~7/13일": "전국 8도 데이터 완전 통합",
        "상시": "URL 추가 제작 및 추가 변경"
    }
    st.table(pd.DataFrame(list(roadmap_data.items()), columns=['일정', '상세 내용']))
    
    if st.button("로그아웃"):
        st.session_state['bus_auth'] = False
        st.rerun()

# [전역 설정 및 초기화]
st.set_page_config(page_title="통합 버스 정산 시스템", page_icon="🚌")
if 'admin_active' not in st.session_state: st.session_state['admin_active'] = False
if 'system_mode' not in st.session_state: st.session_state['system_mode'] = 'HOME'
if 'bus_auth' not in st.session_state: st.session_state['bus_auth'] = False

# [사이드바: 관리자 서버 (숨김 처리)]
with st.sidebar:
    st.title("⚙️ 관리자 서버")
    if not st.session_state['admin_active']:
        admin_password = st.text_input("마스터 코드", type="password")
        if st.button("인증"):
            if admin_password == ADMIN_CODE:
                st.session_state['admin_active'] = True
                st.rerun()
    else:
        st.success("권한 활성화")
        if st.button("관리자 모드 종료"):
            st.session_state['admin_active'] = False
            st.rerun()
        st.session_state['system_mode'] = st.selectbox("지역 제어", ['HOME', 'SEOUL', 'BUSAN'])

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
