FROM python:3.8
COPY . /onestop
WORKDIR /onestop
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install pyyaml
RUN pip install requests
RUN pip install confluent-kafka
RUN pip install avro-python3
RUN pip install fastavro
RUN apt-get install vim -y
CMD tail -f /dev/null


