from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from .config import MONGO_URI

# 채팅 세션 ID를 기반으로 MongoDB에 기록을 저장/조회하는 함수
def get_session_history(session_id: str) -> MongoDBChatMessageHistory:
    """
    주어진 세션 ID에 대한 채팅 기록 객체를 반환합니다.
    MongoDB에 해당 세션 ID의 기록이 없으면 새로 생성합니다.
    """
    return MongoDBChatMessageHistory(
        connection_string=MONGO_URI,
        session_id=session_id,
        database_name="9oorm",      # 사용할 데이터베이스 이름
        collection_name="chat_histories" # 사용할 컬렉션 이름
    )