import os
import streamlit as st
from agents import Agent, Runner, SQLiteSession

# 1. Streamlit 페이지 설정
st.set_page_config(
    page_title="Science Inquiry Coach",
    page_icon=" ",
    layout="centered",
)

# 2. OpenAI API Key 설정
os.environ["OPENAI_API_KEY"]
# Agent, Runner를 import했으므로 생략해도 됨

# 3. Single Education Agent 정의
science_agent = Agent(
    name="Science Inquiry Coach",
    instructions="""
[ROLE] 너는 중학생의 과학 자유탐구를 지원하는 Science Inquiry Coach이다.
[GOAL] 학생이 자신의 관심사를 과학 개념과 연결하여 탐구 가능한 질문을
스스로 발전시키도록 지원한다.
[RULES]
1. 학생의 생각을 먼저 확인한다.
2. 완성된 탐구질문을 처음부터 바로 제공하지 않는다.
3. 필요한 정보가 부족하면 추가 질문을 한다.
4. 질문을 개선할 때 개선 이유를 설명한다.
5. 여러 대안을 제시할 수 있지만 최종 선택은 학생이 한다.
6. 학생 대신 수행평가나 탐구보고서를 완성하지 않는다.
7. 위험하거나 부적절한 실험은 추천하지 않는다.
8. 확실하지 않은 내용을 사실처럼 단정하지 않는다.

[PROCESS]
1. 학생의 학년과 관심분야를 확인한다.
2. 학생의 초기 탐구 아이디어를 확인한다.
3. 현재 질문의 탐구 가능성을 분석한다.
4. 개선이 필요한 부분을 설명한다.
5. 필요한 경우 개선 방향이나 질문 후보를 제안한다.
6. 학생이 직접 선택하거나 수정하도록 한다.
7. 수정된 질문을 다시 분석하고 피드백한다.

[OUTPUT]
상황에 따라 다음 내용을 포함한다.
- 현재 아이디어 또는 질문에 대한 분석
- 개선이 필요한 부분
- 개선 방향
- 필요한 경우 질문 후보
- 학생이 다음으로 생각해야 할 질문
항상 학생이 스스로 생각하고 선택하도록 지원한다.
""",
)

# 4. Streamlit Session State 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Agent Multi-turn Session 초기화
if "agent_session" not in st.session_state:
    st.session_state.agent_session = SQLiteSession(
        "student_session",
        "science_agent.db",
    )

# 6. 화면 제목
st.title("Science Inquiry Coach")
st.caption(
    "AI가 탐구질문을 대신 결정하는 것이 아니라 "
    "학생이 스스로 좋은 탐구질문을 발전시키도록 지원합니다."
)

# 7. 사이드바
with st.sidebar:
    st.header("Agent Information")
    st.write("**Role**")
    st.write("Science Inquiry Coach")
    st.write("**Goal**")
    st.write(
        "학생이 자신의 관심사를 과학 개념과 연결하여 "
        "탐구 가능한 질문을 스스로 발전시키도록 지원"
    )
    st.divider()
    st.write("**Agent Architecture**")
    st.write(
        """Student
↓
Single Agent (LLM Model)
↓
Feedback
↓
Student Choice"""
    )

# 8. 기존 대화 화면 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. 사용자 입력
user_input = st.chat_input("과학 탐구에 관심 있는 주제를 입력하세요.")

# 10. Agent 실행
if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Agent가 생각하고 있습니다..."):
            try:
                result = Runner.run_sync(
                    science_agent,
                    user_input,
                    session=st.session_state.agent_session,
                )
                response = result.final_output
                st.markdown(response)
            except Exception as e:
                response = f"오류가 발생했습니다: {e}"
                st.error(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )