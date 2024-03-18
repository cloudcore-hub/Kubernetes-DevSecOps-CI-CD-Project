FROM python:3.13.0a4-slim
WORKDIR /usr/src/app
COPY mongo.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./mongo.py"]
