from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

from .config import GEMINI_API_KEY
from .database import get_session_history
from .prompts import chatbot_prompt

# 1. Gemini 모델 초기화
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)

# 2. 프롬프트와 모델을 연결하여 기본 체인 생성
base_chain = chatbot_prompt | llm

# 3. 데이터 계층(get_session_history)과 연결하여 채팅 기록을 관리하는 최종 체인 생성
chain_with_history = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",    # 사용자의 입력을 저장할 키
    history_messages_key="history", # 기록을 저장할 키 (프롬프트의 MessagesPlaceholder와 일치)
)