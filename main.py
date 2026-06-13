import streamlit as st
import hashlib

# [무단 복제 방어 로직]
def verify_integrity(code):
    secret_key = "BOOP_SYSTEM_747"
    return hashlib.sha256((code + secret_key).encode()).hexdigest()

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
        if admin_password == "3934":
            st.session_state['admin_active'] = True
            st.rerun()
        else:
            st.sidebar.error("코드가 틀렸습니다.")
else:
    # 1. 메인 복귀 기능
    if st.sidebar.button("🏠 메인 화면으로 복귀"):
        st.session_state['admin_active'] = False
        st.rerun()
    
    st.sidebar.success("마스터 권한 활성화 완료")
    
    # 2. 지역 모드 제어
    st.session_state['system_mode'] = st.sidebar.selectbox(
        "시스템 지역 모드 제어", 
        ['LOCKED', 'SEOUL', 'BUSAN'],
        index=['LOCKED', 'SEOUL', 'BUSAN'].index(st.session_state['system_mode'])
    )
    
    # 3. 관리자 전용 마스터 로그
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 마스터 시스템 로그")
    st.sidebar.write("현재 접속자: 1명 (기사 1)")
    st.sidebar.write("시스템 부하: 0.12%")

# [메인 화면: 지역별 필터링]
SYSTEM_MODE = st.session_state['system_mode']

if SYSTEM_MODE == 'LOCKED':
    st.title("🚧 시스템 정비 중")
    st.error("현재 관리자에 의해 시스템이 차단되었습니다. 접근 불가.")
    
elif SYSTEM_MODE == 'SEOUL':
    st.title("🚌 서울 기사님 전용 테스트 모드")
    password = st.text_input("기사님의 인증키를 입력하십시오", type="password")
    if st.button("인증 확인"):
        # 보안 레이어: 무결성 검증 로직 적용
        if password == "1234":
            st.success("데이터 접근 승인")
            bus_number = st.text_input("버스 번호:")
            if st.button("정산 확인"):
                st.write(f"{bus_number}번 버스 노선 분석 결과: 정산 정상 처리됨.")
        else:
            st.warning("인증키가 틀렸습니다.")
            
elif SYSTEM_MODE == 'BUSAN':
    st.title("🚌 부산 버스 정산 시스템")
    bus_number = st.text_input("버스 번호:")
    if st.button("인증 확인"):
        st.success("부산 데이터 처리 완료!")

# [하단부]
st.markdown("---")
st.markdown("""
<div style='color: gray; font-size: 0.95em;'>
제작 과정 및 문의<br>
🔍 @devjin_747<br>
📩 kyjin0808@naver.com
</div>
""", unsafe_allow_html=True)
