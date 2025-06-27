# Use a more recent, but stable, version of Python
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy and install requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application using a production server
# gunicorn is more robust than Flask's built-in server
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "application:app"]