# Use an official Python runtime as base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt .
COPY app/ app/
COPY /app/main.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask
EXPOSE 5000

# Run Flask app
CMD ["python", "main.py"]
