import streamlit as st
import pandas as pd

st.set_page_config(page_title="시스템 복구 모드", page_icon="🚌")

# [안전 장치] 데이터 파일이 없으면 빈 상태로 시작 (앱이 죽지 않게 함)
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

# [메인 로직]
if st.session_state.locked and not st.session_state.admin:
    st.title("서비스 종료")
    st.stop()

st.title("버스 정산 시스템")
if df.empty:
    st.error("데이터 파일(bus_data.csv)이 비어있거나 없습니다.")
else:
    # 조회 로직
    bus_no = st.text_input("버스 번호", value="402")
    if st.button("조회"):
        result = df[df['bus_no'] == bus_no]
        if not result.empty:
            st.write(result)
        else:
            st.warning("데이터를 찾을 수 없습니다.")

st.markdown("🔍 @devjin_747 | 📩 kyjin0808@naver.com")
