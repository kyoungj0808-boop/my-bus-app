import streamlit as st
import pandas as pd
import io

# 1. 페이지 설정
st.set_page_config(page_title="버스 정보 시스템", page_icon="🚌")

# 2. 정확한 데이터 (기점-회차지 중심)
data = """bus_no,first,last,route,info
503,04:15,22:20,광명공영차고지-서울역버스환승센터,정류장 88개 / 거리 32.5km
5714,04:00,23:30,광명공영차고지-신촌로터리,정류장 72개 / 거리 34.2km
"""
df = pd.read_csv(io.StringIO(data), dtype={'bus_no': str})

# 3. 관리자/세션 상태 관리
if 'admin' not in st.session_state: st.session_state.admin = False

# 4. 사이드바 (관리자)
with st.sidebar:
    st.header("⚙️ 관리자 설정")
    pw = st.text_input("관리자 코드", type="password")
    if st.button("인증/로그아웃"):
        if pw == "3934":
            st.session_state.admin = not st.session_state.admin
            st.rerun()

# 5. 메인 화면
st.title("🚌 통합 버스 정산 시스템")
st.markdown("---")

# 세션 상태 초기화 (입력값 제어)
if 'search_query' not in st.session_state: st.session_state.search_query = ""

def trigger_search():
    st.session_state.search_triggered = True

# 버스 번호 입력 (엔터 기능 강화)
bus_no = st.text_input("버스 번호 입력 (예: 503)", key="search_query", on_change=trigger_search)
search = st.button("조회")

if search or st.session_state.get('search_triggered'):
    st.session_state.search_triggered = False # 초기화
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
