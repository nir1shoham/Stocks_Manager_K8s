# Use an official Python runtime as the base image
FROM python:alpine3.17

# Set the working directory in the container
WORKDIR /CapitalGains
# Copy relevant application files and directories

COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Flask application
CMD ["python", "app.py"]
