from fastapi import FastAPI, Form, UploadFile, File
from pydantic import BaseModel

from app.categorize import categorize_business_logic
from app.chain import chain_with_history

# FastAPI 앱 초기화
app = FastAPI(root_path="/chatbot")

# 요청 본문을 위한 Pydantic 모델 정의
class ChatRequest(BaseModel):
    session_id: str
    message: str


async def get_full_response(session_id: str, message: str):
    """
    LangChain을 사용하여 전체 답변을 생성하고 반환하는 비동기 함수입니다.
    """
    # LangChain의 비동기 invoke 메서드를 호출하기 위해 await를 사용합니다.
    config = {"configurable": {"session_id": session_id}}
    result = await chain_with_history.ainvoke({"input": message}, config=config)

    return result.content

# --- API 모델 정의 ---
class CategorizationResponse(BaseModel):
    category: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    일반적인 채팅봇을 위한 엔드포인트입니다.
    """
    # LangChain을 사용하여 전체 답변을 가져오는 비동기 함수를 호출합니다.
    response_content = await get_full_response(request.session_id, request.message)

    # FastAPI는 딕셔너리 객체를 자동으로 JSON 응답으로 변환합니다.
    return {"response": response_content}

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

