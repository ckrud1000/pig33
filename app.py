import streamlit as st

st.set_page_config(
    page_title="급식줄 길이 확인기",
    page_icon="🍱",
    layout="centered"
)

st.title("🍱 급식줄 길이 확인기")
st.write("현재 급식실 줄 길이를 입력해보세요.")

try:
    line_count = st.number_input(
        "현재 줄 서 있는 인원 수",
        min_value=0,
        max_value=500,
        value=20,
        step=1
    )

    wait_seconds = line_count * 10
    wait_minutes = wait_seconds // 60
    remain_seconds = wait_seconds % 60

    st.subheader("📊 결과")

    st.metric(
        "현재 줄 인원",
        f"{line_count}명"
    )

    st.metric(
        "예상 대기 시간",
        f"{wait_minutes}분 {remain_seconds}초"
    )

    if line_count <= 10:
        st.success("🟢 여유")
    elif line_count <= 30:
        st.info("🟡 보통")
    elif line_count <= 50:
        st.warning("🟠 혼잡")
    else:
        st.error("🔴 매우 혼잡")

    progress = min(line_count / 100, 1.0)
    st.progress(progress)

    st.caption("※ 예상 대기 시간은 1명당 10초 기준입니다.")

except Exception as e:
    st.error("오류가 발생했습니다.")
    st.exception(e)
