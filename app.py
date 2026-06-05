import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💖"
)

st.title("💖 연애상담 챗봇")
st.write("연애 고민을 편하게 이야기해보세요!")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
prompt = st.chat_input("고민을 입력하세요...")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 이전 대화를 문자열로 변환
        conversation = ""

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "상담사"
            conversation += f"{role}: {msg['content']}\n"

        system_prompt = """
        당신은 친절한 연애 상담사입니다.
        공감하며 답변하고 현실적인 조언을 제공합니다.
        답변은 한국어로 작성하세요.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"{system_prompt}\n\n{conversation}"
        )

        answer = response.text

    except Exception as e:
        answer = f"오류가 발생했습니다: {e}"

    # AI 답변 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
