FROM python:3.13.5-slim
WORKDIR /usr/src/app
COPY mongo.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./mongo.py"]
