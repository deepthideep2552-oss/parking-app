# 1. Base image with Python installed
FROM python:3.12-slim

# 2. Working directory inside the container
WORKDIR /app

# 3. Install dependencies first (uses Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application code
COPY . .

# 5. The app listens on port 5000
EXPOSE 5000

# 6. Command to start the app
CMD ["python", "app.py"]
