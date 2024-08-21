FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch.py .
RUN chmod +x fetch.py

ENTRYPOINT ["python", "fetch.py"]