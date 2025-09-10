from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 챗봇의 역할을 정의하는 프롬프트 템플릿
chatbot_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 사용자에게 친절하게 답변하는 AI 어시스턴트입니다. 사용자의 질문에 최대한 상세하고 명확하게 답해주세요."),
        MessagesPlaceholder(variable_name="history"), # 채팅 기록이 들어갈 자리
        ("human", "{input}"), # 사용자의 입력이 들어갈 자리
    ]
)