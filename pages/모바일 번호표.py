import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import google.generativeai as genai

# --- 1. 페이지 기본 설정 및 스타일 ---
st.set_page_config(
    page_title="급식 똑똑이 (Smart Meal Care)",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 세션 상태(Session State) 초기화 (데이터 유지) ---
if "waiting_count" not in st.session_state:
    st.session_state.waiting_count = 12  # 초기 대기 팀 수
if "my_ticket" not in st.session_state:
    st.session_state.my_ticket = None
if "current_status" not in st.session_state:
    st.session_state.current_status = "3학년 전체 입장 중"

# --- 3. Gemini AI 설정 (예외 처리 포함) ---
ai_available = False
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 최신 가벼운 모델인 gemini-2.5-flash-lite 사용
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        ai_available = True
    except Exception as e:
        ai_available = False
        ai_error_msg = str(e)
else:
    ai_error_msg = "Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다."

# --- 4. 사이드바 메뉴 구성 ---
st.sidebar.title("🍱 급식 똑똑이 Menu")
menu = st.sidebar.radio(
    "이동할 화면을 선택하세요:",
    ["🏠 홈 & 실시간 이동 정리", "🎫 모바일 번호표 발급", "📊 요일별 혼잡도 통계", "📅 AI 혼잡도 예측 캘린더"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: 번호표를 뽑으면 대기 시간을 줄이고 분산 이동에 참여할 수 있습니다.")

# --- 5. 기능별 화면 구현 ---

# --- [화면 1] 홈 & 실시간 이동 정리 ---
if menu == "🏠 홈 & 실시간 이동 정리":
    st.title("🏠 실시간 급식실 상황판")
    st.subheader("현재 급식실은 원활한 소통과 안전을 위해 분산 입장을 실시하고 있습니다.")
    
    # 대시보드 메트릭 상단 배치
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="현재 대기 팀", value=f"{st.session_state.waiting_count} 팀")
    with col2:
        st.metric(label="예상 대기 시간", value=f"{st.session_state.waiting_count * 2} 분")
    with col3:
        st.metric(label="현재 급식실 혼잡도", value="혼잡 ⚠️" if st.session_state.waiting_count > 10 else "여유 🌱")
        
    st.markdown("---")
    
    ### 급식실 이동 정리 시스템
    st.markdown("### 📢 실시간 입장 통제 현황")
    st.success(f"🔔 **현재 입장 안내:** {st.session_state.current_status}")
    
    # 관리자 기능 시뮬레이션 (데모용 상태 변경)
    with st.expander("⚙️ [관리자 전용] 입장 제어 시뮬레이션"):
        new_status = st.selectbox(
            "입장 상태 변경", 
            ["3학년 전체 입장 중", "2학년 1~4반 입장 중", "2학년 5~8반 입장 중", "1학년 전체 대기, 2학년 입장 마감 중", "전학년 자유 입장"]
        )
        if st.button("상태 업데이트"):
            st.session_state.current_status = new_status
            st.success("입장 상태가 업데이트되었습니다.")
            st.rerun()

# --- [화면 2] 모바일 번호표 발급 (방문시간 분산) ---
elif menu == "🎫 모바일 번호표 발급":
    st.title("🎫 모바일 실시간 번호표")
    st.write("급식실 앞으로 가기 전, 미리 번호표를 뽑아 대기 시간을 분산시키세요!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("대기표 발급받기")
        student_id = st.text_input("학번을 입력하세요 (예: 30101)", placeholder="30101")
        student_name = st.text_input("이름을 입력하세요", placeholder="홍길동")
        
        if st.button("🚀 번호표 뽑기"):
            if student_id and student_name:
                st.session_state.waiting_count += 1
                st.session_state.my_ticket = {
                    "number": st.session_state.waiting_count + 100,
                    "id": student_id,
                    "name": student_name,
                    "time": datetime.datetime.now().strftime("%H:%M:%S")
                }
                st.success("번호표 발급 완료!")
            else:
                st.warning("학번과 이름을 모두 입력해주세요.")
                
    with col2:
        st.subheader(" 나의 모바일 번호표")
        if st.session_state.my_ticket:
            ticket = st.session_state.my_ticket
            st.info(f"""
            🎫 **대기 번호:** {ticket['number']}번  
            👤 **발급자:** {ticket['id']} {ticket['name']}  
            ⏰ **발급 시간:** {ticket['time']}  
            ⏱️ **내 앞 대기:** {st.session_state.waiting_count} 팀  
            ⏳ **예상 대기 시간:** 약 {st.session_state.waiting_count * 2}분
            """)
            st.caption("※ 대기 시간이 5분 전으로 다가오면 급식실 앞으로 이동해주세요.")
            
            if st.button("❌ 번호표 취소/입장 완료"):
                st.session_state.my_ticket = None
                if st.session_state.waiting_count > 0:
                    st.session_state.waiting_count -= 1
                st.success("처리가 완료되었습니다.")
                st.rerun()
        else:
            st.warning("아직 발급된 번호표가 없습니다. 왼쪽에서 번호표를 뽑아주세요.")

# --- [화면 3] 요일별 혼잡도 통계 ---
elif menu == "📊 요일별 혼잡도 통계":
    st.title("📊 과거 요일별 급식실 혼잡도 통계")
    st.write("지난 3달간의 데이터를 바탕으로 집계된 요일별/시간대별 평균 대기 시간입니다.")
    
    # 더미 데이터 생성
    days = ['월요일', '화요일', '수요일', '목요일', '금요일']
    avg_wait = [15, 22, 8, 18, 25]  # 수요일은 잔반없는 날 등 메뉴에 따른 예시 데이터
    
    chart_data = pd.DataFrame({
        '요일': days,
        '평균 대기시간(분)': avg_wait
    }).set_index('요일')
    
    st.subheader("📅 요일별 평균 대기 시간 (분 단위)")
    st.bar_chart(chart_data, color="#FF4B4B")
    
    st.markdown("""
    > **📊 데이터 분석 가이드**
    > * **금요일/화요일**은 학생들이 선호하는 메뉴(특식)가 자주 나와 대기 시간이 가장 깁니다. 
    > * **수요일**은 '잔반 없는 날' 운영 및 빠른 퇴식 유도로 회전율이 가장 좋습니다. 
    > * 가능하면 대기 시간이 긴 요일에는 **정규 시간보다 10분 늦게 혹은 일찍** 방문하는 것을 권장합니다.
    """)

# --- [화면 4] AI 혼잡도 예측 캘린더 ---
elif menu == "📅 AI 혼잡도 예측 캘린더":
    st.title("📅 AI 스마트 혼잡도 예측 캘린더")
    st.write("날씨, 요일, 그리고 오늘 또는 내일의 핵심 메뉴를 분석하여 AI가 대기 시간을 예측합니다.")
    
    # 사용자 예측 인풋 수집
    col1, col2, col3 = st.columns(3)
    with col1:
        predict_day = st.selectbox("예측 대상 요일", ["월요일", "화요일", "수요일", "목요일", "금요일"])
    with col2:
        weather = st.selectbox("날씨 상황", ["맑음 ☀️", "비/눈 🌧️", "미세먼지 심함 😷"])
    with col3:
        menu_type = st.text_input("주요 메뉴 입력 (예: 돈까스, 스파게티, 생선구이)", value="돈까스")
        
    if st.button("🤖 AI 예측 리포트 생성"):
        if ai_available:
            with st.spinner("Gemini AI가 혼잡 상황을 분석 중입니다..."):
                try:
                    # 프롬프트 설계
                    prompt = f"""
                    학교 급식실 혼잡도 예측 시스템입니다.
                    다음 조건을 분석하여 해당 일의 예상 혼잡도 수준(여유, 보통, 혼잡, 매우혼잡)을 결정하고, 
                    학생들이 덜 붐비는 '방문시간 분산 꿀팁'을 정중하고 친근하게 제안해주세요.

                    [조건]
                    - 요일: {predict_day}
                    - 날씨: {weather}
                    - 주요 메뉴: {menu_type}

                    [출력 형식 가이드]
                    1. 예상 혼잡도 등급 및 예상 대기 시간 (예: 대기 약 XX분)
                    2. 혼잡 이유 분석 (날씨, 요일, 메뉴 선호도 고려)
                    3. 추천 분산 방문 시간대 팁 제시
                    """
                    
                    response = model.generate_content(prompt)
                    st.success("✨ AI 예측 분석 완료")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    
                except Exception as e:
                    st.error(f"AI 응답 생성 중 오류가 발생했습니다: {e}")
        else:
            # API 키가 없거나 에러가 났을 때 작동하는 안정적인 폴백(Fallback) 로직
            st.warning(f"⚠️ AI 모드가 활성화되지 않아 기본 시뮬레이션 데이터로 대체합니다. (사유: {ai_error_msg})")
            
            # 간단한 규칙 기반 시뮬레이션 결과 제공
            wait_time = 15
            if "돈까스" in menu_type or "치킨" in menu_type or "고기" in menu_type:
                wait_time += 10
            if "비" in weather:
                wait_time += 5
                
            st.info(f"""
            ### 🤖 [시뮬레이션 예측 결과]
            * **예상 혼잡도**: {'매우 혼잡 🔥' if wait_time >= 25 else '보통 😐'}
            * **예상 대기 시간**: 약 {wait_time}분
            * **분산 유도 추천**: {predict_day}에 학생들이 좋아하는 '{menu_type}' 메뉴와 날씨 요인이 결합되어 정시 입장은 혼잡할 수 있습니다. 정상 급식 개시 시간보다 **12분 늦게 방문**하시면 대기 시간을 대폭 줄일 수 있습니다!
            """)
