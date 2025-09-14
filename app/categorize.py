# service 로직이 있는 파일 (예: app/services.py)

import base64
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
# google_exceptions는 이제 데코레이터가 처리하므로 여기서 직접 임포트할 필요 없음

from app.config import GEMINI_API_KEY
from app.prompts import SYSTEM_PROMPT
# 데코레이터와 필요한 예외 클래스만 임포트
from app.exceptions import ApiResponseError, handle_gemini_exceptions

logger = logging.getLogger(__name__)

@handle_gemini_exceptions
async def categorize_business_logic(
        store_name: str,
        description: str,
        main_image_data: bytes,
        main_image_content_type: str,
        menu_image_data: bytes,
        menu_image_content_type: str
) -> str:
    """
    입력된 데이터를 바탕으로 Gemini API를 호출하여 업종을 분류하는 핵심 로직.
    (예외 처리는 데코레이터에 위임)
    """
    # 1. Gemini 모델 초기화
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY, temperature=0)

    # 2. 프롬프트와 모델을 연결하여 기본 체인 생성
    chain = SYSTEM_PROMPT | llm

    # 3. 멀티모달 콘텐츠 생성
    message_content = [
        {"type": "text", "text": f"가게 이름: {store_name}\n한 줄 소개: {description}"},
    ]
    if main_image_data:
        main_image_base64 = base64.b64encode(main_image_data).decode('utf-8')
        message_content.append({"type": "image_url", "image_url": f"data:{main_image_content_type};base64,{main_image_base64}"})
    if menu_image_data:
        menu_image_base64 = base64.b64encode(menu_image_data).decode('utf-8')
        message_content.append({"type": "image_url", "image_url": f"data:{menu_image_content_type};base64,{menu_image_base64}"})

    # 4. 체인 호출
    response = await chain.ainvoke({"input": message_content})

    # 5. 결과 반환 (이 부분의 예외 처리는 비즈니스 로직에 가까우므로 남겨둠)
    if not response or not hasattr(response, 'content') or not response.content:
        raise ApiResponseError("API 응답에 'content'가 없거나 비어있습니다.")

    return response.content.strip()