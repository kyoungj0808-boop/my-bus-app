import streamlit as st

# 페이지 설정
st.set_page_config(page_title="서울 버스 정산 시스템", page_icon="🚌")

# 메인 타이틀
st.title("🚌 서울 버스 정산 시스템")
st.write("서울 유명 버스 노선부터 시범 운영 중입니다.")

# 입력 및 정산 로직
bus_number = st.text_input("버스 번호를 입력하십시오:")

if st.button("정산 확인"):
    if bus_number:
        with st.spinner(f"{bus_number}번 버스 분석 중..."):
            st.success("데이터 처리 완료!")
    else:
        st.warning("버스 번호를 입력해주십시오!")

# 하단 홍보 문구
st.markdown("---")
st.caption("19살 개발자의 개발 비하인드와 제작 과정이 궁금하다면?")
st.info("📸 Instagram: **@devjin_747**")
