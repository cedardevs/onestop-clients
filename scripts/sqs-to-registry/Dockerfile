FROM cedardevs/onestop-python-client:latest
COPY . .
#required by the sme script, not our library
RUN pip install argparse

#I should not have to do this, since it is done in the base image
#RUN pip install -r ./onestop-python-client/requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "s3_notification_handler.py" ]
#CMD tail -f /dev/null