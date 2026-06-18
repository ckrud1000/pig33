import streamlit as st

st.set_page_config(
    page_title="급식줄 길이 확인기",
    page_icon="🍱",
    layout="centered"
)

st.title("🍱 급식줄 길이 확인기")
st.write("현재 급식줄에 있는 사람 수를 입력하세요.")

try:
    people = st.number_input(
        "현재 줄 서 있는 사람 수",
        min_value=0,
        max_value=500,
        value=20,
        step=1
    )

    # 상태 판별
    if people <= 20:
        color = "green"
        status = "🟢 여유"
    elif people <= 50:
        color = "orange"
        status = "🟡 보통"
    elif people <= 80:
        color = "darkorange"
        status = "🟠 혼잡"
    else:
        color = "red"
        status = "🔴 매우 혼잡"

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:10px;
            text-align:center;
            color:white;
            font-size:28px;
            font-weight:bold;">
            {status}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 예상 대기 시간
    wait_minutes = round((people * 15) / 60)

    st.metric(
        label="예상 대기 시간",
        value=f"{wait_minutes}분"
    )

    st.subheader("📊 현재 정보")
    st.write(f"현재 줄 인원: **{people}명**")
    st.write(f"혼잡도: **{status}**")

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
        st.success("입력한 댓글")
        st.write(comment)
    else:
        st.warning("댓글을 입력해주세요.")
