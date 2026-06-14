import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="버스 정보 시스템", page_icon="🚌")

# 2. 관리자/세션 상태 관리
if 'admin' not in st.session_state: st.session_state.admin = False

# 3. 사이드바 (관리자)
with st.sidebar:
    st.header("⚙️ 관리자 설정")
    pw = st.text_input("관리자 코드", type="password")
    if st.button("인증/로그아웃"):
        if pw == "3934":
            st.session_state.admin = not st.session_state.admin
            st.rerun()

# 4. 메인 화면
st.title("🚌 통합 버스 정산 시스템")
st.markdown("---")

# 버스 번호 입력
bus_no = st.text_input("버스 번호 입력 (예: 503)")
search = st.button("조회")

if search:
    file_path = "bus_data.csv"
    
    if not os.path.exists(file_path):
        st.error("데이터 파일을 찾을 수 없습니다.")
    else:
        df = pd.read_csv(file_path, dtype={'bus_no': str})
        res = df[df['bus_no'] == bus_no]
        
        if not res.empty:
            d = res.iloc[0]
            # 요청하신 고정 양식 적용
            st.success(f"🚌 {bus_no}번 버스 노선 정보")
            st.markdown(f"""
            **첫차시간:** {d['first']}  
            **막차시간:** {d['last']}  
            **{d['route']}**
            """)
            st.caption(f"상세 정보: {d['info']}")
        else:
            st.warning("등록되지 않은 노선번호입니다.")

st.markdown("---")
st.markdown("### 제작 과정 및 문의")
st.markdown("<div style='color: gray;'>🔍 @devjin_747 | 📩 kyjin0808@naver.com</div>", unsafe_allow_html=True)
