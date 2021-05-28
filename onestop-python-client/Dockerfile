FROM python:3.8

WORKDIR /app

# Copy requirements.txt into workspace and execute it, so installed in workspace.
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN pip3 install --upgrade pip

# Copy source code into workspace
COPY . .