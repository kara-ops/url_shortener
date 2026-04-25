# 1. Base image — Python 3.13
FROM python:3.13-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Copy the rest of the code
COPY . .

# 5. Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]