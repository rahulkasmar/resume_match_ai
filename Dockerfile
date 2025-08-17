# Use an official, lightweight Python image.
FROM python:3.11-slim

# Set environment variables for Python.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file and install dependencies.
# This layer is cached to speed up future builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose port 8000 for the application.
EXPOSE 8000

# The command to run the application in production using Uvicorn directly.
# --host 0.0.0.0: Makes the server accessible from outside the container.
# --port 8000: Specifies the port to listen on.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]