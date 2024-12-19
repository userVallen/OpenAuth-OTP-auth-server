# Python 3.9 이미지를 기반으로 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 종속성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 필요한 Python 패키지 설치
RUN pip install flask python-dotenv pymongo gunicorn

# 애플리케이션 코드 복사
COPY . .

# 포트 설정
EXPOSE 5000

CMD ["python3", "app.py"]