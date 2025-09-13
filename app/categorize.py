import base64

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_API_KEY
from app.prompts import SYSTEM_PROMPT


async def categorize_business_logic(
        store_name: str,
        description: str,
        main_image_data: bytes,
        main_image_content_type: str,
        menu_image_data: bytes,
        menu_image_content_type: str
) -> str:
    """
    입력된 데이터를 바탕으로 Gemini API를 호출하여 업종을 분류하는 핵심 로직
    """

    # 1. Gemini 모델 초기화
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY, temperature=0)

    # 2. 프롬프트와 모델을 연결하여 기본 체인 생성
    chain = SYSTEM_PROMPT | llm

    # 3. 프롬프트의 {input} 키에 전달할 멀티모달 콘텐츠 생성
    message_content = [
        {
            "type": "text",
            "text": f"가게 이름: {store_name}\n한 줄 소개: {description}"
        },
    ]

    # 대표 이미지가 있는 경우 Base64로 인코딩하여 추가
    if main_image_data:
        main_image_base64 = base64.b64encode(main_image_data).decode('utf-8')
        message_content.append({
            "type": "image_url",
            "image_url": f"data:{main_image_content_type};base64,{main_image_base64}"
        })

    # 메뉴 이미지가 있는 경우 Base64로 인코딩하여 추가
    if menu_image_data:
        menu_image_base64 = base64.b64encode(menu_image_data).decode('utf-8')
        message_content.append({
            "type": "image_url",
            "image_url": f"data:{menu_image_content_type};base64,{menu_image_base64}"
        })

    # 4. 생성한 콘텐츠를 'input' 키에 담아 체인 호출
    response = await chain.ainvoke({"input": message_content})

    # 5. 결과 반환 (AIMessage 객체에서 content 속성만 추출)
    return response.content.strip()
