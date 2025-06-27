FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the logs directory and set its permissions
RUN mkdir -p /app/logs
RUN chmod -R 777 /app/logs

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "application:app"]