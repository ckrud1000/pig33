
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="급식줄 문제해결 도우미",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ 급식줄 문제해결 도우미")
st.markdown("급식 대기 문제를 분석하고 개선 방안을 제안합니다.")

st.divider()

try:
    col1, col2 = st.columns(2)

    with col1:
        students = st.number_input(
            "전체 학생 수",
            min_value=1,
            value=500,
            step=10
        )

        counters = st.number_input(
            "배식 창구 수",
            min_value=1,
            value=2,
            step=1
        )

    with col2:
        serve_time = st.number_input(
            "1명당 평균 배식 시간(초)",
            min_value=1,
            value=8,
            step=1
        )

        lunch_time = st.number_input(
            "급식 시간(분)",
            min_value=1,
            value=40,
            step=5
        )

    st.divider()

    total_seconds = lunch_time * 60

    capacity_per_counter = total_seconds / serve_time
    total_capacity = capacity_per_counter * counters

    waiting_students = max(0, int(students - total_capacity))

    if total_capacity >= students:
        status = "🟢 원활"
    elif total_capacity >= students * 0.8:
        status = "🟡 보통"
    else:
        status = "🔴 매우 혼잡"

    st.subheader("분석 결과")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "처리 가능 인원",
        f"{int(total_capacity)}명"
    )

    c2.metric(
        "예상 대기 인원",
        f"{waiting_students}명"
    )

    c3.metric(
        "혼잡도",
        status
    )

    st.divider()

    st.subheader("📊 현황 그래프")

    chart_df = pd.DataFrame({
        "구분": ["전체 학생", "처리 가능 인원"],
        "인원": [students, int(total_capacity)]
    })

    st.bar_chart(
        chart_df.set_index("구분")
    )

    st.divider()

    st.subheader("💡 해결 방안")

    solutions = []

    if waiting_students > 0:
        solutions.append("배식 창구 수를 추가합니다.")
        solutions.append("학년별 급식 시간을 분산 운영합니다.")
        solutions.append("배식 동선을 단순화하여 이동 시간을 줄입니다.")
        solutions.append("급식 시간을 연장합니다.")
        solutions.append("메뉴 사전 선택제를 도입합니다.")
    else:
        solutions.append("현재 운영 상태가 양호합니다.")
        solutions.append("정기적으로 배식 시간을 점검합니다.")
        solutions.append("학생 이동 동선을 유지·관리합니다.")

    for idx, item in enumerate(solutions, start=1):
        st.write(f"{idx}. {item}")

    st.divider()

    st.subheader("📝 과제용 보고서")

    report = f"""
급식줄 문제 분석 결과

- 전체 학생 수: {students}명
- 배식 창구 수: {counters}개
- 1명당 평균 배식 시간: {serve_time}초
- 급식 시간: {lunch_time}분

분석 결과 처리 가능 인원은 약 {int(total_capacity)}명이며,
예상 대기 인원은 {waiting_students}명으로 계산되었다.

혼잡도는 '{status}' 수준으로 판단된다.

개선 방안:
{chr(10).join([f"- {s}" for s in solutions])}
"""

    st.text_area(
        "보고서 내용",
        report,
        height=250
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
