# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the backend directory contents into the container at /app
COPY . /app

# Copy the templates directory into the container at /app/templates
COPY ./frontend/templates /app/templates

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run mongo.py to initialize the database
RUN python mongo.py

# Run app.py when the container launches
CMD ["python", "app.py"]
