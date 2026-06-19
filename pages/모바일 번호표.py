import streamlit as st
import pandas as pd
import numpy as np
import datetime
import google.generativeai as genai

# --- 1. 페이지 기본 설정 및 스타일 ---
st.set_page_config(
    page_title="급식 패스 (MealPass)",
    page_icon="🍱",
    layout="wide"
)

# --- 2. AI 설정 (Gemini) ---
def get_ai_prediction(day, menu_type, special_event):
    """Gemini-2.5-flash-lite를 사용한 혼잡도 예측 및 분산 가이드 생성"""
    try:
        # Streamlit Secret에서 API 키 로드
        if "GEMINI_API_KEY" not in st.secrets:
            return "⚠️ API 키가 설정되지 않아 AI 예측을 사용할 수 없습니다. (Secrets 설정을 확인하세요)"
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        prompt = f"""
        당신은 학교 급식 운영 전문가입니다. 다음 조건에 따라 급식실 혼잡 시간대를 예측하고 방문 분산 팁을 제공해주세요.
        - 요일: {day}
        - 메뉴 종류: {menu_type}
        - 특이사항: {special_event if special_event else '없음'}
        
        조언에는 다음 내용이 포함되어야 합니다:
        1. 가장 혼잡할 것으로 예상되는 구체적인 시간대 (예: 12:40 ~ 12:55)
        2. 이 날 가장 쾌적하게 식사할 수 있는 추천 방문 시간대
        3. 학생들을 위한 한 줄 팁 (친근한 말투로)
        
        답변은 4줄 이내로 간결하고 명확하게 작성해주세요.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ AI 분석 중 오류가 발생했습니다: {str(e)}"

# --- 3. 가상 데이터 및 상태(State) 관리 ---
if 'waiting_count' not in st.session_state:
    st.session_state.waiting_count = 14  # 현재 대기 팀 수
if 'my_ticket' not in st.session_state:
    st.session_state.my_ticket = None

# 가상 요일별 통계 데이터
day_data = pd.DataFrame({
    '요일': ['월', '화', '수', '목', '금'],
    '평균 대기시간(분)': [15, 22, 12, 18, 25],
    '이용 학생 수(명)': [420, 480, 390, 450, 510]
})

# --- 4. 메인 화면 레이아웃 ---
st.title("🍱 급식 패스 (MealPass)")
st.subheader("실시간 급식실 이동 정리 및 혼잡도 예측 시스템")
st.markdown("---")

# 사이드바: 실시간 이동 통제 현황
st.sidebar.header("📢 실시간 이동 통제")
st.sidebar.success("🟢 현재 입장 가능: 3학년 전체")
st.sidebar.warning("🟡 교실 대기: 1학년, 2학년")
st.sidebar.info("💡 앞 번호가 줄어들면 알림이 울립니다.")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📱 모바일 번호표 & 이동", "📅 AI 혼잡도 예측 캘린더", "📊 요일별 통계"])

# --- TAB 1: 모바일 번호표 & 이동 정리 ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎫 모바일 번호표 발급")
        with st.form("ticket_form"):
            grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
            class_num = st.selectbox("반", [f"{i}반" for i in range(1, 11)])
            name = st.text_input("이름", placeholder="홍길동")
            submit = st.form_submit_button("번호표 발급받기")
            
            if submit:
                if name.strip() == "":
                    st.error("이름을 입력해주세요.")
                else:
                    st.session_state.waiting_count += 1
                    st.session_state.my_ticket = {
                        "number": st.session_state.waiting_count + 100,
                        "time": datetime.datetime.now().strftime("%H:%M:%S"),
                        "before_me": st.session_state.waiting_count
                    }
                    st.success("🎉 번호표가 정상 발급되었습니다!")

    with col2:
        st.markdown("### 🔔 내 번호표 확인")
        if st.session_state.my_ticket:
            st.info(f"**대기 번호:** {st.session_state.my_ticket['number']}번")
            st.metric(label="내 앞 대기 인원", value=f"{st.session_state.my_ticket['before_me']} 팀")
            st.metric(label="예상 대기 시간", value=f"{st.session_state.my_ticket['before_me'] * 2} 분")
            st.caption(f"발급 시간: {st.session_state.my_ticket['time']}")
        else:
            st.write("발급된 번호표가 없습니다. 왼쪽에서 번호표를 발급받으세요.")

    st.markdown("---")
    st.markdown("### 🏃‍♂️ 급식실 현재 상태")
    c1, c2, c3 = st.columns(3)
    c1.metric("현재 대기 팀", f"{st.session_state.waiting_count} 팀", "+2팀")
    c2.metric("예상 회전율", "빠름 (면류)", "정상")
    c3.metric("현재 혼잡도", "혼잡 (대기 20분 이상)", "주의", delta_color="inverse")

# --- TAB 2: 혼잡 시간대 예측 캘린더 & 방문시간 분산 ---
with tab2:
    st.markdown("### 📅 AI 기반 급식실 혼잡도 예측")
    st.write("요일과 메뉴를 선택하면 AI가 혼잡 시간을 예측하고 쾌적한 식사 시간을 추천합니다.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        predict_day = st.selectbox("예측할 요일 선택", ["월요일", "화요일", "수요일", "목요일", "금요일"])
        menu_type = st.radio("메뉴 스타일", ["일반 백반류 (고기/생선 등)", "면류/분식 (스파게티, 우동 등)", "특식/선호 메뉴 (치킨, 피자, 버거 등)"])
        special_event = st.text_input("특이사항 입력 (예: 비 오는 날, 4교시 단축수업 등)", "")
        
        btn_predict = st.button("🔮 AI 예측 실행")
        
    with col_b:
        st.markdown("#### 🤖 AI 분석 결과 및 방문 분산 추천")
        if btn_predict:
            with st.spinner("AI가 급식실 데이터를 분석 중입니다..."):
                analysis_result = get_ai_prediction(predict_day, menu_type, special_event)
                st.info(analysis_result)
        else:
            st.write("← 왼쪽 설정을 마치고 버튼을 누르면 AI 리포트가 생성됩니다.")

# --- TAB 3: 요일별 통계 데이터 ---
with tab3:
    st.markdown("### 📊 과거 데이터를 통한 요일별 패턴 분석")
    st.write("어느 요일에 급식실이 가장 붐빌까요? 통계를 확인하고 눈치 게임에 성공해보세요!")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### ⏱️ 요일별 평균 대기 시간(분)")
        st.bar_chart(data=day_data, x='요일', y='평균 대기시간(분)', color="#FF4B4B")
        
    with col_chart2:
        st.markdown("#### 👥 요일별 이용 학생 수(명)")
        st.line_chart(data=day_data, x='요일', y='이용 학생 수(명)', color="#0068C9")
        
    st.warning("💡 **통계 요약:** 금요일과 화요일은 평균 대기 시간이 길어지므로, 평소보다 10분 늦게 혹은 일찍 이동하는 것을 권장합니다.")
