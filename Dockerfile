FROM python:3.8

COPY ./onestop-python-client /onestop-python-client
COPY ./scripts /scripts

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install ./onestop-python-client
RUN pip install -r ./onestop-python-client/requirements.txt

#Base image stays up for dev access
CMD tail -f /dev/null
