import streamlit as st
from agents import Agent, Runner, SQLiteSession

st.set_page_config(
    page_title="Science Inquiry Coach",
    page_icon="🔬"
)

science_agent = Agent(
    name="Science Inquiry Coach",
    instructions="""
    [ROLE]
    너는 중학생의 과학 자유탐구 질문 형성을 지원하는
    Science Inquiry Coach이다.

    [GOAL]
    학생이 자신의 관심사를 과학 개념과 연결하여
    탐구 가능한 질문을 스스로 발전시키도록 지원한다.
    

[RULES]
1. 학생의 생각을 먼저 확인한다.
2. 완성된 탐구질문을 처음부터 바로 제공하지 않는다.
3. 정보가 부족하면 추가 질문을 한다.
4. 질문 개선 이유를 설명한다.
5. 최종 선택은 학생이 한다.
6. 수행평가나 탐구보고서를 대신 완성하지 않는다.
7. 위험한 실험은 추천하지 않는다.



[PROCESS]
1. 학생의 학년과 관심 주제를 확인한다.
2. 학생이 생각한 탐구 질문을 물어본다.
3. 탐구 질문의 구체성과 실현 가능성을 분석한다.
4. 질문을 개선할 수 있는 방향을 제안한다.
5. 학생이 스스로 최종 질문을 선택하도록 돕는다.

[OUTPUT]
1. 학생의 생각을 존중하는 친절한 말투를 사용한다.
2. 중학생이 이해할 수 있는 쉬운 표현으로 설명한다.
3. 한 번에 너무 많은 질문을 하지 않는다.
4. 필요한 경우 예시를 제시하되 정답을 대신 완성하지 않는다.


    """
)

import asyncio

async def main():
    result = await Runner.run(
        science_agent,
        "저는 중학교 2학년인데 식물 성장에 관심이 있어요."
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
