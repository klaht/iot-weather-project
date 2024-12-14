FROM python:3.9-slim

WORKDIR /app
COPY influx-logger.py requirements.txt /app/
RUN pip install -r requirements.txt

CMD ["python", "-u", "influx-logger.py"]