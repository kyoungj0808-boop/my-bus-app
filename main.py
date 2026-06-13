import streamlit as st

# [전역 설정]
SYSTEM_MODE = 'SEOUL_PILOT' 
st.set_page_config(page_title="서울 버스 정산 시스템", page_icon="🚌")

# 관리자 인증 (사령관님용: 3934)
admin_password = st.sidebar.text_input("관리자 인증:", type="password")
if admin_password == "3934":
    SYSTEM_MODE = st.sidebar.selectbox("지역 모드:", ['LOCKED', 'SEOUL_PILOT', 'BUSAN_LIVE'])

# [지역 필터링]
if SYSTEM_MODE == 'LOCKED':
    st.title("🚧 시스템 정비 중")
elif SYSTEM_MODE == 'SEOUL_PILOT':
    st.title("🚌 서울 기사님 전용 테스트 모드")
    password = st.text_input("서울 기사님 인증키를 입력하십시오", type="password")
    if password == "mybus747":
        st.success("접근 허용")
        bus_number = st.text_input("버스 번호:")
        if st.button("정산 확인"):
            st.write("서울 노선 분석 완료.")
    else:
        st.warning("기사님 전용 인증키가 필요합니다.")
elif SYSTEM_MODE == 'BUSAN_LIVE':
    st.title("🚌 부산 버스 정산 시스템")
    bus_number = st.text_input("버스 번호:")
    if st.button("정산 확인"):
        st.success("부산 데이터 처리 완료!")

# [하단부 - 폰트 사이즈 업]
st.markdown("---")
st.markdown("""
<div style='color: gray; font-size: 1.1em;'>
제작 과정 및 문의<br>
📸 @devjin_747<br>
📩 kyjin0808@naver.com
</div>
""", unsafe_allow_html=True)
