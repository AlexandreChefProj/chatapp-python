# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables to avoid creating .pyc files
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first (to cache dependencies)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container (this includes everything in your project)
COPY . /app/

# Make sure the wait-for-it.sh script is executable
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expose the port that Flask will run on
EXPOSE 5000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
