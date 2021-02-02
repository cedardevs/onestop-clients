#FROM python:3
#COPY . /onestop-clients
#WORKDIR /onestop-clients
#RUN pip install --upgrade pip
#RUN pip install -r onestop-python-client/requirements.txt
#RUN apt-get update
#RUN pip install ./onestop-python-client
#RUN apt-get install vim -y
#CMD tail -f /dev/null

FROM python:3.8
COPY ./onestop-python-client /onestop-python-client
#WORKDIR /onestop-python-client
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install pyyaml
RUN pip install requests
RUN pip install confluent-kafka
RUN pip install avro-python3
RUN pip install fastavro
RUN pip install boto3
RUN pip install botocore
RUN pip install argparse
RUN pip install smart_open

#ENTRYPOINT [ "python" ]
CMD tail -f /dev/null
