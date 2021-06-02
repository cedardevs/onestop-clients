# Expect this to copy the scripts directory over and install onestop-python-client.
FROM cedardevs/onestop-python-client:latest

#required by the sme script, not our library
RUN pip install argparse

ENTRYPOINT [ "python" ]
CMD [ "s3_notification_handler.py" ]
#CMD tail -f /dev/null