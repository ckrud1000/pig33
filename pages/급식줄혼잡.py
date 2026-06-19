import streamlit as st

st.set_page_config(
    page_title="급식줄 길이 확인기",
    page_icon="🍱",
    layout="centered"
)

st.title("🍱 급식줄 길이 확인기")
st.write("현재 급식줄 인원을 입력하면 혼잡도와 예상 대기시간을 알려줍니다.")

try:
    people = st.number_input(
        "현재 줄 서 있는 사람 수",
        min_value=0,
        max_value=500,
        value=20,
        step=1
    )

    # 혼잡도 판별
    if people <= 20:
        color = "#28a745"
        status = "🟢 여유"
    elif people <= 50:
        color = "#ffc107"
        status = "🟡 보통"
    elif people <= 80:
        color = "#fd7e14"
        status = "🟠 혼잡"
    else:
        color = "#dc3545"
        status = "🔴 매우 혼잡"

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:12px;
            text-align:center;
            color:white;
            font-size:28px;
            font-weight:bold;">
            {status}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1명 = 1분
    wait_minutes = people

    st.metric(
        label="⏰ 예상 대기 시간",
        value=f"{wait_minutes}분"
    )

    st.subheader("📊 현재 상황")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"현재 인원\n\n**{people}명**")

    with col2:
        st.info(f"혼잡도\n\n**{status}**")

except Exception as e:
    st.error("오류가 발생했습니다.")
    st.error(str(e))

st.divider()

st.subheader("💬 수업 댓글")

comment = st.text_area(
    "오늘 급식줄 상황을 적어보세요",
    placeholder="예) 오늘은 줄이 짧아서 빨리 먹을 수 있었다."
)

if st.button("댓글 확인"):
    if comment.strip():
        st.success("댓글이 저장되었습니다.")
        st.write(comment)
    else:
        st.warning("댓글을 입력해주세요.")

st.divider()

st.caption("🍱 급식줄 길이 확인기 | 학교 프로젝트용")
