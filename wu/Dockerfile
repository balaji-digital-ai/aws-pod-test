# Use a base Python image
FROM python:3.8-slim

# Install dependencies and AWS CLI
RUN apt-get update && apt-get install -y unzip curl && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    pip install boto3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your Python code to the container
COPY script.py /app/script.py

# Set environment variables for function name and region
ENV FUNCTION_NAME ""
ENV REGION ""
ENV ASSUME_ROLE ""

# Set the command to run your Python program
CMD ["python", "script.py"]
