FROM tensorflow/tensorflow:latest-py3

WORKDIR /app
COPY classify.h5 /app/
COPY predict.py /app/
COPY classify_hotEncoder.pkl /app/
COPY requirements.txt /app/


RUN pip install -r requirements.txt

CMD ["python", "-u", "predict.py"]