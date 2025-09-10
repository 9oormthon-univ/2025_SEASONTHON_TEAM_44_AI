from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.chain import chain_with_history
import asyncio

# FastAPI 앱 초기화
app = FastAPI()

# 요청 본문을 위한 Pydantic 모델 정의
class ChatRequest(BaseModel):
    session_id: str
    message: str

async def stream_generator(session_id: str, message: str):
    """답변을 스트리밍 방식으로 생성하는 비동기 제너레이터"""

    # LangChain의 비동기 스트리밍 호출
    config = {"configurable": {"session_id": session_id}}
    async for chunk in chain_with_history.astream({"input": message}, config=config):
        if hasattr(chunk, 'content'):
            yield chunk.content
            # 작은 지연을 주어 스트리밍 효과를 극대화 (실제 서비스에서는 조절 필요)
            await asyncio.sleep(0.01)


@app.post("/chat")
async def chat(request: ChatRequest):
    """챗봇과 대화하는 API 엔드포인트"""
    gen = stream_generator(request.session_id, request.message)
    return StreamingResponse(gen, media_type="text/plain")