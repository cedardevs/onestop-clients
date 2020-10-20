FROM python:3
COPY . /onestop-clients
WORKDIR /onestop-clients
RUN pip install --upgrade pip
RUN pip install -r onestop-python-client/requirements.txt
RUN apt-get update
RUN pip install ./onestop-python-client
RUN apt-get install vim -y
CMD tail -f /dev/null
