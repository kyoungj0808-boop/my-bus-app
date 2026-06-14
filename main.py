import streamlit as st
import hashlib
import os
import pandas as pd

# [보안 설정]
SECRET_KEY = os.getenv("APP_SECRET_KEY", "BOOP_SYSTEM_747")
ADMIN_CODE = os.getenv("ADMIN_MASTER_CODE", "3934")

# [버스 데이터베이스]
BUS_DATA = {
    "503": {"first": "04:15", "last": "22:20", "route": "광명공영차고지기점-서울역버스환승센터", "info": "(48/32.5km)"},
    "101": {"first": "05:00", "last": "23:00", "route": "화영운수차고지-석수역", "info": "(41/14km)"}
}

# [기사님 전용 대시보드 함수]
def show_driver_dashboard():
    st.success("데이터 접근 승인 완료: 운행 모드 가동")
    
    # 버스 정보 조회 모듈
    bus_number = st.text_input("버스 번호 입력 (예: 503, 101):")
    if bus_number:
        if bus_number in BUS_DATA:
            b = BUS_DATA[bus_number]
            st.info(f"🚌 {bus_number}번 버스 노선 정보")
            st.write(f"첫차시간: {b['first']}")
            st.write(f"막차시간: {b['last']}")
            st.write(f"{b['route']} {b['info']}")
        else:
            st.warning("데이터베이스에 없는 노선입니다.")

    st.markdown("---")
    
    # 정산 모듈
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

# [전역 설정 및 세션 초기화]
st.set_page_config(page_title="통합 버스 정산 시스템", page_icon="🚌")
if 'admin_active' not in st.session_state: st.session_state['admin_active'] = False
if 'system_mode' not in st.session_state: st.session_state['system_mode'] = 'HOME'
if 'bus_auth' not in st.session_state: st.session_state['bus_auth'] = False

# [사이드바: 관리자 서버 (숨김/토글)]
with st.sidebar:
    st.title("⚙️ 관리자 서버")
    if not st.session_state['admin_active']:
        admin_password = st.text_input("마스터 코드", type="password")
        if st.button("인증"):
            if admin_password == ADMIN_CODE:
                st.session_state['admin_active'] = True
                st.rerun()
    else:
        st.success("관리자 권한 활성화")
        if st.button("관리자 모드 종료"):
            st.session_state['admin_active'] = False
            st.rerun()
        st.session_state['system_mode'] = st.selectbox("지역 제어", ['HOME', 'LOCKED', 'SEOUL', 'BUSAN'])

# [메인 화면 로직]
SYSTEM_MODE = st.session_state['system_mode']

if SYSTEM_MODE == 'HOME':
    st.title("🚌 통합 버스 정산 시스템")
    st.write("서비스 이용을 위해 모드를 선택하십시오.")
    if st.button("서울 기사님 모드 입장"):
        st.session_state['system_mode'] = 'SEOUL'
        st.rerun()

elif SYSTEM_MODE == 'LOCKED':
    st.title("🚧 시스템 정비 중")
    st.error("보안 정책에 의해 차단됨.")

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

elif SYSTEM_MODE == 'BUSAN':
    st.title("🚌 부산 버스 정산 시스템")
    st.write("부산 지역 데이터 처리 모드 활성화됨.")

# [하단부]
st.markdown("---")
st.markdown("<div style='color: gray; font-size: 0.95em;'>🔍 @devjin_747 | 📩 kyjin0808@naver.com</div>", unsafe_allow_html=True)
