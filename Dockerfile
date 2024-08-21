FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fetch.py .
COPY test_fetch.py .
RUN chmod +x fetch.py

# Test stage
RUN python -m unittest test_fetch.py

ENTRYPOINT ["python", "fetch.py"]