FROM python:3.8

COPY ./onestop-python-client /onestop-python-client
COPY ./scripts /scripts

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r ./onestop-python-client/requirements.txt

# Needed for scripts - do here since directory out of scope when in scripts/* dockerfiles.
# Unsure if possible this isn't latest build, like doing pip install before this is built.
RUN pip install ./onestop-python-client

#Base image stays up for dev access
CMD tail -f /dev/null
