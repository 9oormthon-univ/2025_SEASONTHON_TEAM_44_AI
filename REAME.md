# 🤖 AI 기반 업종 추천 및 챗봇 서비스 (TEAM 44)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-26.1-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=github-actions)](https://github.com/features/actions)

**구름톤 유니브 시즌톤**을 위해 개발된 AI 애플리케이션입니다. 이 서비스는 Google의 최신 LLM인 **Gemini**를 활용하여 두 가지 핵심 기능을 제공합니다.

1.  **멀티모달 업종 추천**: 사용자가 가게 이름, 설명, 대표 이미지, 메뉴판 이미지를 업로드하면, AI가 이를 종합적으로 분석하여 최적의 업종을 추천합니다.
2.  **대화형 챗봇**: **MongoDB**와 연동하여 대화 기록을 관리하는 챗봇 기능을 통해 사용자와 자연스러운 소통이 가능합니다. 사장님이 대화하는 챗봇이며 사용법 등을 제공합니다.

## ✨ 주요 기능

-   **업종 추천**: 텍스트와 이미지(멀티모달) 입력을 기반으로 한 AI 업종 분류
-   **챗봇**: 세션 ID 기반으로 대화 맥락을 기억하는 대화형 챗봇
-   **CI/CD 자동화**: `main` 브랜치 변경 시 GitHub Actions를 통한 자동 빌드 및 서버 배포

## 🛠️ 기술 스택

| 구분          | 기술                                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| **Backend** | <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" /> <img src="https://img.shields.io/badge/Gunicorn-499848?logo=gunicorn&logoColor=white" /> |
| **AI / LLM** | <img src="https://img.shields.io/badge/LangChain-4B9D23?logo=langchain&logoColor=white" /> <img src="https://img.shields.io/badge/Google_Gemini-8E44AD?logo=google&logoColor=white" /> |
| **Database** | <img src="https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white" />                         |
| **DevOps** | <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white" /> |

## 🚀 시작하기

### 1. 환경 변수 설정

프로젝트를 실행하기 위해 루트 디렉토리에 `.env` 파일을 생성하고 아래 내용을 채워주세요.

```env
# .env

# Google Gemini API 키
GEMINI_API_KEY="여기에_API_키를_입력하세요"

# MongoDB 연결 URI
# 예: mongodb://<user>:<password>@<host>:<port>/
MONGO_URI="여기에_MongoDB_연결_URI를_입력하세요"

# (선택) LangChain에서 사용할 MongoDB 데이터베이스 이름
MONGO_DB_NAME="9oorm"

# (선택) LangChain에서 사용할 MongoDB 컬렉션 이름
MONGO_COLLECTION="chat_histories"