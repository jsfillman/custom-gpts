FROM python:3.13-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY web-adventure.py .
COPY templates/ templates/

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "web-adventure.py"]

