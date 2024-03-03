FROM python:3.11-slim
WORKDIR /app
COPY backend/ ./
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/static ./static
COPY frontend/templates ./templates
EXPOSE 8080
ENV NAME World
CMD ["python", "app.py"]
