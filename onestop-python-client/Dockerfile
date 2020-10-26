FROM python:3
COPY . /onestop
COPY . /tests
WORKDIR /onestop
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install vim -y
CMD tail -f /dev/null
