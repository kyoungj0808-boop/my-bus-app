import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="버스 시스템", page_icon="🚌")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'mode' not in st.session_state: st.session_state.mode = 'HOME'
if 'admin' not in st.session_state: st.session_state.admin = False

# [사이드바: 관리자]
with st.sidebar:
    st.title("⚙️ 관리자")
    pw = st.text_input("코드", type="password")
    if st.button("인증"):
        if pw == "3934": st.session_state.admin = True
    if st.session_state.admin and st.button("로그아웃"):
        st.session_state.admin = False
        st.rerun()

# [메인 로직]
if st.session_state.mode == 'HOME':
    st.title("🚌 통합 버스 정산 시스템")
    if st.button("서울 기사님 모드 입장"):
        st.session_state.mode = 'SEOUL'
        st.rerun()
else:
    if not st.session_state.auth:
        st.title("🚌 인증 필요")
        key = st.text_input("인증키", type="password")
        if st.button("입장"):
            if key == "1234":
                st.session_state.auth = True
                st.rerun()
    else:
        st.success("운행 모드 가동 중")
        bus = st.text_input("버스 번호 입력 (예: 503)")
        # [조회] 버튼을 눌러야 명확하게 결과를 출력함
        if st.button("조회"):
            if os.path.exists("bus_data.csv"):
                df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})
                res = df[df['bus_no'] == bus]
                if not res.empty:
                    d = res.iloc[0]
                    st.info(f"🚌 {bus}번 버스 노선 정보")
                    st.write(f"첫차시간: {d['first']}")
                    st.write(f"막차시간: {d['last']}")
                    st.write(f"{d['route']}{d['info']}")
                else:
                    st.warning("등록되지 않은 노선번호입니다.")
            else:
                st.error("데이터 파일을 찾을 수 없습니다.")
        
        if st.button("메인화면"):
            st.session_state.auth = False
            st.session_state.mode = 'HOME'
            st.rerun()

st.markdown("---")
st.markdown("제작 과정 및 문의")
st.markdown("<div style='color: gray; font-size: 0.95em;'>🔍 @devjin_747 | 📩 kyjin0808@naver.com</div>", unsafe_allow_html=True)
