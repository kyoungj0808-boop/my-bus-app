import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="버스 정보 시스템", page_icon="🚌")

# 2. 데이터 로드
df = pd.read_csv("bus_data.csv", dtype={'bus_no': str})

# 3. 요금 체계 정의 (사령관님 고정값)
FARE_MAP = {'어린이': 550, '청소년': 900, '성인': 1500}

# 4. 관리자 로직 (사이드바)
if 'admin' not in st.session_state: 
    st.session_state.admin = False

with st.sidebar:
    st.header("⚙️ 관리자 설정")
    pw = st.text_input("관리자 코드", type="password")
    if st.button("인증/로그아웃"):
        if pw == "3934":
            st.session_state.admin = not st.session_state.admin
            st.rerun()

st.title("🚌 통합 버스 정산 시스템")
st.markdown("---")

# 5. 승객 유형 선택 UI
st.markdown("### 🚌 승객 유형을 선택하세요")
passenger_type = st.radio(
    "요금 계산 기준:",
    ('어린이', '청소년', '성인'),
    index=2, # 기본값: 성인
    horizontal=True
)
st.session_state['passenger_type'] = passenger_type
st.markdown("---")

# 6. 조회 로직
bus_no = st.text_input("버스 번호 입력 (예: 151)")
search = st.button("조회")

if search or bus_no:
    res = df[df['bus_no'] == bus_no]
    if not res.empty:
        d = res.iloc[0]
        # 초록색 박스 헤더
        st.success(f"🚌 {bus_no}번 버스 노선 정보")
        
        # 기본 정보 출력 (첫차, 막차, 경로)
        st.markdown(f"""
        **첫차시간:** {d['first']}  
        **막차시간:** {d['last']}  
        **{d['route']}**
        """)
        
        # 사령관님 요청: 상세 정보와 요금을 작고 흐린 폰트(st.caption)로 줄바꿈하여 출력
        current_fare = FARE_MAP[passenger_type]
        st.caption(f"상세 정보: {d['info']}")
        st.caption(f"💰 {passenger_type} 요금: {current_fare:,}원")
        
        st.markdown("---")
    else:
        st.warning("등록되지 않은 노선번호입니다.")

# 7. 하단 정보
st.markdown("---")
st.markdown("### 제작 과정 및 문의")
st.markdown("<div style='color: gray;'>🔍 @devjin_747 | 📩 kyjin0808@naver.com</div>", unsafe_allow_html=True)
