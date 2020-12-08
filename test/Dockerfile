FROM python:3.8
RUN apt-get update \
  && apt-get install -y  libgirepository1.0-dev libcairo2-dev python3-dev gir1.2-secret-1 \
  && apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

ENV SERVICEBUS_NAMESPACE=
ENV SERVICE_BUS_QUEUE_NAME=
ENV LOCAL=false
CMD ["bash","-c","python main.py"]