FROM python:3
ADD *.py /
RUN pip install confluent-kafka
RUN pip install confluent-kafka[avro]
RUN apt-get update
RUN apt-get install vim -y
CMD [ "python", "smeFunc.py", "-b KAFKA_BROKERS", "-s SCHEMA_REGISTRY", "-t TOPIC", "-g GROUP_ID" ]
