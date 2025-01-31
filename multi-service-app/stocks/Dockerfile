# Use an official Python runtime as the base image
FROM python:alpine3.17

# Set the working directory inside the container
WORKDIR /Stocks
# Copy the rest of the application files into the container


COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the Flask app
CMD ["python", "app.py"]
