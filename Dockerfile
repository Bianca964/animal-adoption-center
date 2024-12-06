# Use a base Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["python3", "run.py"]
