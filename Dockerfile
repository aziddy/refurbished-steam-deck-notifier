FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY notifier.py .
COPY scheduler.py .

# Create directory for logs
RUN mkdir -p /app/logs

# Run the scheduler with unbuffered output
ENTRYPOINT ["python", "-u", "scheduler.py"]
