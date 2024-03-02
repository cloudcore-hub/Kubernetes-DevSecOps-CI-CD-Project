FROM python:3.11-slim
WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
ENV NAME World
CMD ["python", "app.py"]
