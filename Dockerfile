# 1. 베이스 이미지 선택 (Python 3.11 슬림 버전)
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 먼저 복사 및 설치 (gunicorn 추가 필요)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 나머지 소스 코드 복사
COPY . .

# 5. 컨테이너가 8000번 포트를 외부에 노출하도록 설정
EXPOSE 8000

# 6. gunicorn으로 애플리케이션 실행 (uvicorn 워커 사용)
# 워커의 수는 보통 (CPU 코어 수 * 2) + 1 로 설정하는 것을 권장합니다.
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--workers", "2", "--bind", "0.0.0.0:8000"]