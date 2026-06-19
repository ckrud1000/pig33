import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="급식 패스 (MealPass)",
    page_icon="🍱",
    layout="centered"
)

# --- 가상 데이터 생성 (초기화) ---
if 'ticket_number' not in st.session_state:
    st.session_state.ticket_number = 142  # 현재 대기 번호 시작점
if 'my_ticket' not in st.session_state:
    st.session_state.my_ticket = None
if 'current_serving' not in st.session_state:
    st.session_state.current_serving = 135  # 현재 호출 중인 번호

# --- 메인 타이틀 ---
st.title("🍱 스마트 급식줄 솔루션: 급식 패스")
st.markdown("시차 급식과 모바일 번호표로 대기 없는 즐거운 점심시간을 만드세요!")
st.divider()

# --- 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🎟️ 모바일 번호표 & 이동", "📅 혼잡도 예측 캘린더", "📊 요일별 통계"])

# ==========================================
# TAB 1: 모바일 번호표 & 급식실 이동 정리
# ==========================================
with tab1:
    st.header("🎟️ 실시간 모바일 번호표")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="현재 입장 중인 번호", value=f"{st.session_state.current_serving}번")
    with col2:
        st.metric(label="전체 대기 팀 수", value=f"{st.session_state.ticket_number - st.session_state.current_serving}팀")
        
    st.subheader("👇 내 번호표 발급받기")
    if st.session_state.my_ticket is None:
        if st.button("모바일 번호표 발행", type="primary"):
            st.session_state.my_ticket = st.session_state.ticket_number
            st.session_state.ticket_number += 1
            st.rerun()
    else:
        st.success(f"🎉 번호표가 발급되었습니다! 나의 번호: **{st.session_state.my_ticket}번**")
        waiting_turns = st.session_state.my_ticket - st.session_state.current_serving
        
        if waiting_turns > 0:
            st.info(f"💡 앞으로 **{waiting_turns}팀** 남았습니다. 교실에서 대기해 주세요!")
        else:
            st.balloons()
            st.error("📢 즉시 급식실로 이동하여 식사해 주세요!")
            
        if st.button("번호표 반납/초기화"):
            st.session_state.my_ticket = None
            st.rerun()

    st.divider()
    
    st.header("🚶 학급별 이동 정리 안내")
    st.markdown("학년별/학급별 정해진 이동 상태를 확인하고 움직여주세요.")
    
    # 가상의 학급 이동 데이터
    class_status = pd.DataFrame({
        "학년": ["1학년", "1학년", "2학년", "2학년", "3학년", "3학년"],
        "반": ["1~3반", "4~6반", "1~3반", "4~6반", "1~3반", "4~6반"],
        "현재 상태": ["🟢 즉시 이동", "🟡 교실 대기", "🟢 즉시 이동", "🔴 이동 제한", "🟢 식사 중", "🟢 식사 중"]
    })
    
    # 테이블 스타일링 대신 가독성 좋은 데이터프레임 출력
    st.dataframe(class_status, use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: 급식실 혼잡 시간대 예측 캘린더 & 방문시간 분산
# ==========================================
with tab2:
    st.header("📅 이번 주 혼잡도 예측 캘린더")
    st.markdown("요일과 시간대를 선택해 예상 혼잡도를 확인하고, **여유로운 시간대**를 공략하세요!")
    
    # 요일 및 시간 선택
    selected_day = st.selectbox("요일 선택", ["월요일", "화요일", "수요일", "목요일", "금요일"])
    
    # 가상의 시간대별 혼잡도 데이터 생성 함수
    def get_congestion(day):
        times = ["12:00", "12:15", "12:30", "12:45", "13:00", "13:15"]
        if day == "수요일":  # 수요일 맛있는 메뉴 나오는 날 가정
            status = ["혼잡 🔥", "매우 혼잡 🚨", "매우 혼잡 🚨", "혼잡 🔥", "보통 🌱", "여유 ✨"]
        else:
            status = ["보통 🌱", "혼잡 🔥", "매우 혼잡 🚨", "보통 🌱", "여유 ✨", "여유 ✨"]
        return pd.DataFrame({"시간대": times, "예상 혼잡도": status})

    df_predict = get_congestion(selected_day)
    
    # 사용자에게 추천 메시지 제공
    st.write(f"### 🔍 {selected_day} 시간대별 추천도")
    
    for idx, row in df_predict.iterrows():
        time_str = row['시간대']
        status_str = row['예상 혼잡도']
        
        if "여유" in status_str:
            st.success(f"🟢 **{time_str}** : {status_str} (쾌적하게 식사가 가능합니다. 추천!)")
        elif "보통" in status_str:
            st.info(f"🟡 **{time_str}** : {status_str} (무난한 시간대입니다.)")
        else:
            st.warning(f"🔴 **{time_str}** : {status_str} (대기 시간이 길어질 수 있습니다. 분산 방문 권장!)")

# ==========================================
# TAB 3: 요일별 통계
# ==========================================
with tab3:
    st.header("📊 지난주 요일별 평균 대기 시간")
    st.markdown("지난주 데이터를 바탕으로 산정된 요일별 평균 대기 시간(분) 그래프입니다.")
    
    # 가상 통계 데이터
    stats_data = pd.DataFrame({
        "요일": ["월", "화", "수", "목", "금"],
        "평균 대기 시간(분)": [15, 18, 25, 14, 10]
    })
    
    # Streamlit 기본 바 차트 사용 (오류 발생 확률 최소화)
    st.bar_chart(data=stats_data, x="요일", y="평균 대기 시간(분)")
    
    st.markdown("""
    > **💡 통계 분석 팁:** > 특식(맛있는 메뉴)이 자주 나오는 **수요일**이 대기 시간이 가장 깁니다.   
    > 수요일에는 평소보다 10분 늦게 혹은 일찍 이동하시는 것을 강력히 추천합니다!
    """)
