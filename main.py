if not res.empty:
        d = res.iloc[0]
        st.success(f"🚌 {bus_no}번 버스 노선 정보")
        st.markdown(f"""
        **첫차시간:** {d['first']}  
        **막차시간:** {d['last']}  
        **{d['route']}**
        """)
        
        # 사령관님 요청: 상세 정보와 요금을 같은 폰트 스타일로 줄바꿈하여 출력
        current_fare = FARE_MAP[passenger_type]
        st.markdown(f"""
        상세 정보: {d['info']}  
        💰 {passenger_type} 요금: {current_fare:,}원
        """)
        
        st.markdown("---")
    else:
        st.warning("등록되지 않은 노선번호입니다.")
