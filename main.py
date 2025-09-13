from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.categorize import categorize_business_logic
from app.chain import chain_with_history

# FastAPI 앱 초기화
app = FastAPI(root_path="/chatbot")

# 요청 본문을 위한 Pydantic 모델 정의
class ChatRequest(BaseModel):
    session_id: str
    message: str

async def stream_generator(session_id: str, message: str):
    """답변을 스트리밍 방식으로 생성하는 비동기 제너레이터"""

    # LangChain의 비동기 스트리밍 호출
    config = {"configurable": {"session_id": session_id}}
    async for chunk in chain_with_history.invoke({"input": message}, config=config):
        if hasattr(chunk, 'content'):
            return chunk.content
    return None


# --- API 모델 정의 ---
class CategorizationResponse(BaseModel):
    category: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """사장님이 일반적으로 사용하는 채팅봇"""
    gen = stream_generator(request.session_id, request.message)
    return StreamingResponse(gen, media_type="text/plain")


@app.post("/categorize", response_model=CategorizationResponse)
async def categorize_business_controller(
        store_name: str = Form(..., description="가게 이름"),
        description: str = Form(..., description="가게 한 줄 소개"),
        main_image: UploadFile = File(..., description="가게 대표 이미지 파일"),
        menu_image: UploadFile = File(..., description="메뉴판 이미지 파일")
):
    """
    HTTP 요청을 받아 서비스 계층으로 데이터를 전달하고, 그 결과를 응답으로 반환합니다.
    """
    try:
        # 1. 업로드된 파일 데이터를 bytes로 변환
        main_image_data = await main_image.read()
        menu_image_data = await menu_image.read()

        # 2. 서비스 계층의 핵심 로직 함수 호출
        category = await categorize_business_logic(
            store_name=store_name,
            description=description,
            main_image_data=main_image_data,
            main_image_content_type=main_image.content_type,
            menu_image_data=menu_image_data,
            menu_image_content_type=menu_image.content_type
        )

        return {"category": category}

    except Exception as e:
        # 서비스 계층에서 발생한 예외를 여기서 잡아 HTTP 에러로 변환
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"업종 분류 중 서버 오류 발생: {str(e)}")
