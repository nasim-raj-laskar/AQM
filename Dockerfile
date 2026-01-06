FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements from root
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code ONLY
COPY backend ./backend

# Set working directory to backend
WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
