FROM python:3.10-slim

WORKDIR /app

#install the dependencies
COPY news_fetcher/requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

#copy the source code

COPY news_fetcher/ ./news_fetcher

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

    
EXPOSE 8000

CMD ["python", "-m", "news_fetcher.main"]