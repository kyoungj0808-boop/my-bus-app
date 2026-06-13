import streamlit as st

# [전역 설정]
# 서비스 상태: 'LOCKED'(차단), 'SEOUL_LIVE'(서울공개), 'BUSAN_PILOT'(부산기사님전용)
SYSTEM_MODE = 'BUSAN_PILOT' 

st.set_page_config(page_title="서울/부산 버스 정산 시스템", page_icon="🚌")

# 관리자 인증 (사령관님용)
admin_password = st.sidebar.text_input("관리자 인증:", type="password")
if admin_password == "1234":
    SYSTEM_MODE = st.sidebar.selectbox("지역 모드 선택:", ['LOCKED', 'SEOUL_LIVE', 'BUSAN_PILOT'])
    st.sidebar.success(f"현재 운영 모드: {SYSTEM_MODE}")

# [지역 필터링 로직]
if SYSTEM_MODE == 'LOCKED':
    st.title("🚧 시스템 정비 중")
    st.error("현재 모든 서비스가 일시 중단되었습니다.")

elif SYSTEM_MODE == 'BUSAN_PILOT':
    st.title("🚌 부산 기사님 전용 테스트 모드")
    password = st.text_input("부산 기사님 인증키를 입력하십시오:", type="password")
    if password == "busan123": # 기사님들께만 드릴 별도 키
        st.success("부산 데이터 접근 허용")
        bus_number = st.text_input("버스 번호를 입력하십시오:")
        if st.button("정산 확인"):
            st.write("부산 노선 분석 완료.")
    else:
        st.warning("외부 접속이 차단되었습니다. 기사님만 접속 가능합니다.")

elif SYSTEM_MODE == 'SEOUL_LIVE':
    st.title("🚌 서울 버스 정산 시스템")
    bus_number = st.text_input("버스 번호를 입력하십시오:")
    if st.button("정산 확인"):
        st.success("서울 데이터 처리 완료!")

# 공통 하단부
st.markdown("---")
st.caption("제작 과정 및 문의: 📸 @devjin_747 | 📩 kyjin0808@naver.com")
