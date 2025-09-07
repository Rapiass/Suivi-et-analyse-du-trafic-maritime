# Use a Python base image
FROM python:3.10-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install MySQL client
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expose any necessary ports (if applicable)
EXPOSE 5000

# Command to wait for API and run the ETL script
CMD ["/bin/sh", "-c", "/app/wait-for-it.sh api:8000 --timeout=30 --strict -- python main.py"]


#docker network create AIS_NET
#docker build -t etl_ais_img
#docker run --network AIS_NET --name etl_cont ETL_AIS_IMG
