import streamlit as st
import hashlib
import os
import pandas as pd

# [보안 레이어 1: 환경 변수 활용]
SECRET_KEY = os.getenv("APP_SECRET_KEY", "BOOP_SYSTEM_747")
ADMIN_CODE = os.getenv("ADMIN_MASTER_CODE", "3934")

# [보안 레이어 2: 무결성 검증 함수]
def verify_integrity(code):
    return hashlib.sha256((code + SECRET_KEY).encode()).hexdigest()

# [전역 설정]
st.set_page_config(page_title="통합 버스 정산 시스템", page_icon="🚌")

# 세션 상태 초기화
if 'admin_active' not in st.session_state: st.session_state['admin_active'] = False
if 'system_mode' not in st.session_state: st.session_state['system_mode'] = 'SEOUL'
if 'bus_auth' not in st.session_state: st.session_state['bus_auth'] = False

# [사이드바: 관리자 서버 통제실]
st.sidebar.title("🛡️ 관리자 서버")
if not st.session_state['admin_active']:
    admin_password = st.sidebar.text_input("관리자 마스터 코드", type="password")
    if st.sidebar.button("관리자 인증"):
        if admin_password == ADMIN_CODE:
            st.session_state['admin_active'] = True
            st.rerun()
else:
    if st.sidebar.button("🏠 관리자 모드 종료"):
        st.session_state['admin_active'] = False
        st.rerun()
    st.session_state['system_mode'] = st.sidebar.selectbox("지역 모드 제어", ['LOCKED', 'SEOUL', 'BUSAN'])

# [메인 화면]
SYSTEM_MODE = st.session_state['system_mode']

if SYSTEM_MODE == 'LOCKED':
    st.title("🚧 시스템 정비 중")
    st.error("보안 정책에 의해 차단됨.")

elif SYSTEM_MODE == 'SEOUL':
    st.title("🚌 서울 기사님 전용 테스트 모드")
    if not st.session_state['bus_auth']:
        password = st.text_input("기사님 인증키 입력", type="password")
        if st.button("인증 확인"):
            if password == "1234":
                st.session_state['bus_auth'] = True
                st.rerun()
            else:
                st.warning("인증 오류")
    else:
        st.success("데이터 접근 승인 완료")
        bus_number = st.text_input("버스 번호:")
        if st.button("정산 확인"):
            st.write(f"{bus_number}번 노선 정산 완료.")
        
        # [로드맵 섹션]
        st.markdown("---")
        st.subheader("🗓️ 전국 단위 확장 로드맵")
        roadmap_data = {
            "~6/16일": "무료배포 종료(월 요금제 도입)",
            "~6/22일": "서울시 기차정보 및 부산 버스 정보 공지(테스트)",
            "~6/29일": "충청/전라도 작업(테스트 및 공표)",
            "~7/6일": "경상도/강원도 작업(테스트 및 공표)",
            "~7/13일": "황해도, 평안도, 함경도(전국 8도 완성)",
            "상시": "URL 추가 제작 및 추가 변경"
        }
        st.table(pd.DataFrame(list(roadmap_data.items()), columns=['일정', '상세 내용']))
        
        if st.button("로그아웃"):
            st.session_state['bus_auth'] = False
            st.rerun()

elif SYSTEM_MODE == 'BUSAN':
    st.title("🚌 부산 버스 정산 시스템")
    st.write("부산 지역 데이터 처리 모드 활성화됨.")

# [하단부: 문의처]
st.markdown("---")
st.markdown("""
<div style='color: gray; font-size: 0.95em;'>
제작 과정 및 문의<br>
🔍 @devjin_747<br>
📩 kyjin0808@naver.com
</div>
""", unsafe_allow_html=True)
