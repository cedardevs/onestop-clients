FROM cedardevs/onestop-python-client:latest
COPY . .
RUN pip install argparse
RUN pip install psycopg2
#ENTRYPOINT [ "python" ,"scripts/sme/sme.py", "-cmd consume", "-b localhost:9092", "-s http://localhost:8081", "-t psi-collection-extractor-to" , "-g sme-test",  "-o earliest" ]
CMD tail -f /dev/null
