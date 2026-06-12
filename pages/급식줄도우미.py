import streamlit as st
import time

st.set_page_config(
    page_title="급식줄 도우미",
    page_icon="🍱",
    layout="wide"
)

st.title("🍱 급식줄 도우미")

st.markdown("""
급식줄을 체계적으로 서고,
줄을 똑바로 맞추기 위한 간단한 도우미입니다.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    total_students = st.number_input(
        "현재 줄 인원",
        min_value=1,
        value=20
    )

with col2:
    my_position = st.number_input(
        "내 번호",
        min_value=1,
        max_value=int(total_students),
        value=1
    )

st.divider()

service_time = st.slider(
    "1명당 배식 시간(초)",
    2,
    10,
    5
)

wait_time = (my_position - 1) * service_time

st.subheader("⏱ 예상 대기 시간")

minutes = wait_time // 60
seconds = wait_time % 60

st.success(
    f"약 {minutes}분 {seconds}초 후에 배식을 받을 수 있어요."
)

st.divider()

st.subheader("📍 내 줄 위치")

positions = list(range(1, total_students + 1))

cols = st.columns(5)

for i, pos in enumerate(positions):
    with cols[i % 5]:
        if pos == my_position:
            st.markdown(
                f"""
                <div style="
                    background:#4CAF50;
                    color:white;
                    padding:15px;
                    border-radius:10px;
                    text-align:center;
                    font-size:24px;
                    font-weight:bold;">
                    😀 {pos}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="
                    background:#eeeeee;
                    padding:15px;
                    border-radius:10px;
                    text-align:center;">
                    {pos}
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()

st.subheader("📏 줄 정렬 모드")

line_length = st.slider(
    "한 줄에 표시할 학생 수",
    5,
    20,
    10
)

for i in range(1, total_students + 1):

    if i == my_position:
        st.markdown(
            f"""
            <span style="
            background:#2E7D32;
            color:white;
            padding:8px 14px;
            margin:3px;
            border-radius:8px;
            display:inline-block;">
            😀 {i}
            </span>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <span style="
            background:#e0e0e0;
            padding:8px 14px;
            margin:3px;
            border-radius:8px;
            display:inline-block;">
            {i}
            </span>
            """,
            unsafe_allow_html=True
        )

    if i % line_length == 0:
        st.write("")

st.divider()

st.subheader("🔔 줄서기 팁")

st.info("""
1. 자신의 번호를 확인하세요.
2. 초록색 번호 위치에 서세요.
3. 앞 사람과 일정한 간격을 유지하세요.
4. 줄이 휘어지면 정렬 모드를 보고 맞추세요.
""")
