import streamlit as st
import pandas as pd

st.set_page_config(page_title="버스 정산 시스템", page_icon="🚌")

# CSV를 확실하게 로드
try:
    df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})
except:
    df = pd.DataFrame(columns=['bus_no', 'route', 'info'])

if 'admin' not in st.session_state: st.session_state.admin = False
if 'locked' not in st.session_state: st.session_state.locked = False

with st.sidebar:
    st.header("관리자 모드")
    pw = st.text_input("코드", type="password")
    if st.button("인증"):
        if pw == "3934":
            st.session_state.admin = True
            st.rerun()
    
    if st.session_state.admin:
        if st.button("배포 종료(잠금)"): st.session_state.locked = True; st.rerun()
        if st.button("배포 재개(해제)"): st.session_state.locked = False; st.rerun()

if st.session_state.locked and not st.session_state.admin:
    st.title("서비스 종료")
    st.stop()

st.title("🚌 통합 버스 정산 시스템")
bus_no = st.text_input("버스 번호 입력", value="402")

if st.button("조회"):
    # 데이터프레임에서 정확히 버스 번호 찾기
    result = df[df['bus_no'] == bus_no.strip()]
    if not result.empty:
        for idx, row in result.iterrows():
            st.success(f"{row['bus_no']}번 버스 정보 확인")
            st.write(f"경로: {row['route']}")
            st.write(f"상세: {row['info']}")
    else:
        st.warning("해당 번호의 버스 데이터를 찾을 수 없습니다.")
