import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="급식줄 문제해결 도우미",
    page_icon="🍱",
    layout="centered"
)

st.title("🍱 급식줄 문제해결 도우미")

st.markdown("""
학교 급식 시간의 대기 문제를 간단히 분석하고
해결 방법을 찾아보세요.
""")

try:
    students = st.number_input(
        "전체 학생 수",
        min_value=1,
        value=300,
        step=1
    )

    counters = st.number_input(
        "현재 배식 창구 수",
        min_value=1,
        value=2,
        step=1
    )

    serving_time = st.number_input(
        "학생 1명당 평균 배식 시간(초)",
        min_value=1,
        value=8,
        step=1
    )

    if st.button("분석하기"):

        total_time_sec = (students * serving_time) / counters
        total_time_min = total_time_sec / 60

        avg_wait_sec = total_time_sec / 2
        avg_wait_min = avg_wait_sec / 60

        last_wait_min = total_time_min

        st.subheader("📊 분석 결과")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "총 배식 시간",
                f"{total_time_min:.1f}분"
            )

        with col2:
            st.metric(
                "평균 대기시간",
                f"{avg_wait_min:.1f}분"
            )

        with col3:
            st.metric(
                "마지막 학생 대기",
                f"{last_wait_min:.1f}분"
            )

        st.subheader("🚦 혼잡도 평가")

        if total_time_min < 15:
            level = "매우 원활"
            color = "🟢"
        elif total_time_min < 30:
            level = "보통"
            color = "🟡"
        else:
            level = "혼잡"
            color = "🔴"

        st.success(f"{color} 현재 상태: {level}")

        st.subheader("💡 개선 방안")

        target_time = 15

        recommended_counters = max(
            1,
            math.ceil((students * serving_time) / (target_time * 60))
        )

        if recommended_counters > counters:
            st.info(
                f"배식 창구를 {recommended_counters}개 이상 운영하면 "
                f"총 배식 시간을 약 {target_time}분 이하로 줄일 수 있습니다."
            )
        else:
            st.info(
                "현재 배식 창구 수가 적절한 수준입니다."
            )

        st.subheader("📈 배식 창구 수 증가 효과")

        data = []

        max_counter = counters + 5

        for c in range(1, max_counter + 1):
            time_min = ((students * serving_time) / c) / 60

            data.append({
                "배식창구수": c,
                "예상배식시간(분)": round(time_min, 2)
            })

        df = pd.DataFrame(data)

        st.line_chart(
            df.set_index("배식창구수")
        )

        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")

st.markdown("---")
st.caption("급식줄 문제해결 과제용 Streamlit 앱")
