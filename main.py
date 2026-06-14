import streamlit as st
import pandas as pd

st.set_page_config(page_title="버스 정보 시스템", page_icon="🚌")

# [융합 포인트] 코드 안의 데이터 변수를 삭제하고, CSV를 읽어옵니다.
# 사령관님이 방금 만드신 bus_data.csv를 프로그램이 자동으로 인식합니다.
df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})

# 관리자 로직 (이전과 동일)
if 'admin' not in st.session_state: st.session_state.admin = False
with st.sidebar:
    st.header("⚙️ 관리자 설정")
    pw = st.text_input("관리자 코드", type="password")
    if st.button("인증/로그아웃"):
        if pw == "3934":
            st.session_state.admin = not st.session_state.admin
            st.rerun()

st.title("🚌 통합 버스 정산 시스템")
st.markdown("---")

# 조회 로직 (엔터키 지원)
bus_no = st.text_input("버스 번호 입력 (예: 5714)")
search = st.button("조회")

if search or bus_no:
    res = df[df['bus_no'] == bus_no]
    if not res.empty:
        d = res.iloc[0]
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
