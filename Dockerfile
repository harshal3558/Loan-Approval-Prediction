# Use an official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy your project files to the container
COPY . /src
COPY . /artifacts

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) Set environment variables
# ENV MODEL_PATH=/app/model.pkl

# Default command to run your ML script (change "model.py" to your entry point)
CMD ["python", "main.py"]