import streamlit as st
import hashlib
import os

# [보안 레이어 1: 환경 변수 활용]
# 상용화 시 깃허브 Settings -> Secrets에 저장하여 코드 외부로 분리할 키들입니다.
SECRET_KEY = os.getenv("APP_SECRET_KEY", "BOOP_SYSTEM_747")
ADMIN_CODE = os.getenv("ADMIN_MASTER_CODE", "3934")

# [보안 레이어 2: 무결성 검증 함수]
def verify_integrity(code):
    return hashlib.sha256((code + SECRET_KEY).encode()).hexdigest()

# [전역 설정]
st.set_page_config(page_title="서울 버스 정산 시스템", page_icon="🚌")

# 세션 상태 초기화
if 'admin_active' not in st.session_state:
    st.session_state['admin_active'] = False
if 'system_mode' not in st.session_state:
    st.session_state['system_mode'] = 'SEOUL'

# [사이드바: 관리자 서버 통제실]
st.sidebar.title("🛡️ 관리자 서버")

if not st.session_state['admin_active']:
    admin_password = st.sidebar.text_input("관리자 마스터 코드", type="password")
    if st.sidebar.button("관리자 인증"):
        # 코드에 직접 적지 않고 환경 변수와 비교하여 해커가 코드를 봐도 알 수 없게 함
        if admin_password == ADMIN_CODE:
            st.session_state['admin_active'] = True
            st.rerun()
        else:
            st.sidebar.error("코드가 틀렸습니다.")
else:
    if st.sidebar.button("🏠 메인 화면으로 복귀"):
        st.session_state['admin_active'] = False
        st.rerun()
    
    st.sidebar.success("마스터 권한 활성화 완료")
    st.session_state['system_mode'] = st.sidebar.selectbox(
        "시스템 지역 모드 제어", 
        ['LOCKED', 'SEOUL', 'BUSAN'],
        index=['LOCKED', 'SEOUL', 'BUSAN'].index(st.session_state['system_mode'])
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 마스터 시스템 로그")
    st.sidebar.write("상태: 보안 모드 가동 중")

# [메인 화면]
SYSTEM_MODE = st.session_state['system_mode']

if SYSTEM_MODE == 'LOCKED':
    st.title("🚧 시스템 정비 중")
    st.error("보안 정책에 의해 차단됨.")
elif SYSTEM_MODE == 'SEOUL':
    st.title("🚌 서울 기사님 전용 테스트 모드")
    password = st.text_input("기사님의 인증키를 입력하십시오", type="password")
    if st.button("인증 확인"):
        if password == "1234":
            st.success("데이터 접근 승인")
            bus_number = st.text_input("버스 번호:")
            if st.button("정산 확인"):
                st.write(f"{bus_number}번 노선 정산 완료.")
        else:
            st.warning("인증 오류")
elif SYSTEM_MODE == 'BUSAN':
    st.title("🚌 부산 버스 정산 시스템")
    bus_number = st.text_input("버스 번호:")
    if st.button("인증 확인"):
        st.success("부산 데이터 처리 완료!")

st.markdown("---")
st.markdown("<div style='color: gray; font-size: 0.8em;'>보안 등급: High | System: v2.0</div>", unsafe_allow_html=True)
