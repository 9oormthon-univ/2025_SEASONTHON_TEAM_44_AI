import functools
import logging
from google.api_core import exceptions as google_exceptions

logger = logging.getLogger(__name__)


class BusinessCategorizationError(Exception):
    """업종 분류 기능 관련 기본 예외 클래스"""
    def __init__(self, message: str = "업종 분류 중 오류가 발생했습니다."):
        self.message = message
        super().__init__(self.message)

class GeminiApiError(BusinessCategorizationError):
    """Gemini API 호출 관련 예외 클래스"""
    def __init__(self, message: str = "Gemini API 통신 중 오류가 발생했습니다."):
        super().__init__(message)

class InvalidInputDataError(BusinessCategorizationError):
    """입력 데이터 처리 관련 예외 클래스"""
    def __init__(self, message: str = "입력 데이터가 잘못되었습니다."):
        super().__init__(message)

class ApiResponseError(BusinessCategorizationError):
    """API 응답 처리 관련 예외 클래스"""
    def __init__(self, message: str = "API로부터 유효하지 않은 응답을 받았습니다."):
        super().__init__(message)


def handle_gemini_exceptions(func):
    """
    Gemini API 호출 시 발생하는 구체적인 예외들을 처리하고
    서비스 레벨의 커스텀 예외로 변환하는 데코레이터.
    비동기 함수를 위해 만들어졌습니다.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # 래핑할 함수(categorize_business_logic)를 그대로 호출
            return await func(*args, **kwargs)

        # --- 예외 처리 로직 (이 부분은 올바릅니다) ---
        except (google_exceptions.PermissionDenied, google_exceptions.Unauthenticated) as e:
            logger.error(f"Gemini API 인증 오류: {e}")
            raise GeminiApiError("Gemini API 인증에 실패했습니다. API 키를 확인하세요.")

        except google_exceptions.ResourceExhausted as e:
            logger.error(f"Gemini API 할당량 초과: {e}")
            raise GeminiApiError("API 요청 할당량을 초과했습니다. 잠시 후 다시 시도해주세요.")

        except (google_exceptions.GoogleAPICallError, google_exceptions.RetryError) as e:
            logger.error(f"Gemini API 호출 오류: {e}")
            raise GeminiApiError("Gemini API 호출 중 문제가 발생했습니다.")

        except TypeError as e:
            logger.error(f"데이터 인코딩 오류: {e}")
            raise InvalidInputDataError("이미지 데이터를 처리하는 중 오류가 발생했습니다.")

        except ApiResponseError as e:
            logger.error(f"API 응답 분석 오류: {e}")
            raise

        except Exception as e:
            logger.error(f"알 수 없는 오류 발생: {e}", exc_info=True)
            raise GeminiApiError("업종 분류 중 예상치 못한 오류가 발생했습니다.")

    return wrapper