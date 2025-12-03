FROM python:3.12-slim

WORKDIR /app/python-app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ingest.sh

CMD ["./ingest.sh"]
