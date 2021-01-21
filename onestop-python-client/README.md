# OneStop Clients

This python package provides an API to connect to OneStop's event stream (aka Inventory Manager). At this early stage there is only a single module for consuming messages from the kafka brokers that back OneStop.
## AWS Credentials
Copy credentials-template.yml to credentials.yml and insert your ACCESS_KEY and SECRET_KEY

## KafkaPublisher
Relies on fastavro <1.0 and confluent-kafka <1.5 

## prerequisites
You will need a kafka broker and a schema-registry running to test this package. To bring up the OneStop stack, see the [OneStop quickstart documentation](https://github.com/cedardevs/onestop/blob/master/docs/developer/quickstart.md#quick-start-kubernetes--helm--skaffold)

## usage
Once you have the OneStop stack (or your own kafka broker + schema registry) running, you are ready to install the package and start consuming messages.

The `onestop_client` can be downloaded via pip, like so-

`python3 -m pip install onestop-python-client-cedardevs`

To test the import, try-

```
$ python3
>>> import onestop_client
```

Now we are ready to try a script. Our first example, [smeFunc.py](#examples/smeFunc.py), imports our onestop_client package, and passes to it the id, topic, and message handler function. Our library then handles the work to connect to kafka and deserialize the message.

Here is how to run it in k8s so that it can connect to the kafka broker and schema registry-
```
kubectl apply -f examples/pyconsumer-pod.yml
```

At the moment, that pod will tail -f /dev/null to stay open so you can exec into the container with -
`
kubectl exec -it pod/pyconsumer -- bash
`
# In the container
Manually add smeFunc.py
Install requests library
>pip install requests

# In the cluster load some test data into the cluster
./upload.sh IM /Users/dneufeld/repos/onestop-test-data/DEM http://localhost/registry

#Test it out using cli args
python smeFunc.py -cmd consume -b onestop-dev-cp-kafka:9092 -s http://onestop-dev-cp-schema-registry:8081 -t psi-registry-collection-parsed-changelog -g sme-test -o earliest


python smeFunc.py -cmd produce -b onestop-dev-cp-kafka:9092 -s http://onestop-dev-cp-schema-registry:8081 -t psi-collection-input-unknown 

Or you can use env vars available so you can run this -
```
python ./smeFunc.py -b $KAFKA_BROKERS -s $SCHEMA_REGISTRY -t $TOPIC -g $GROUP_ID -o $OFFSET
```

# packaing and publishing new version 
=======
The general purpose of this python package is to provide an API to connect to OneStop's event stream (aka Inventory Manager). 
This would enable someone to feed data into OneStop, have OneStop digest it, and then read it out via a python script, such as the example [smeFunc.py](#examples/smeFunc.py).
See the OneStop readme for an example of loading test data into OneStop.
At this early stage there is only a single module for consuming messages from the kafka brokers that back OneStop.

## Prerequisites
1. Since you will need a kafka broker and a schema-registry running you will need OneStop and start it up
    [OneStop quickstart documentation](https://github.com/cedardevs/onestop/blob/master/docs/developer/quickstart.md#quick-start-kubernetes--helm--skaffold)
    Setup and start up the OneStop stack

2. Install this python-client and other dependencies via pip
    `pip install -r requirements.txt`
    
    To test the import, try this and it shouldn't give an error:
    
    ```
    $ python3
    >>> import onestop_client
    ```

Now you are ready to start consuming messages.

## Load Test Data
If you need to load test data then look in the OneStop repo's [OneStop quickstart documentation](https://github.com/cedardevs/onestop/blob/master/docs/developer/quickstart.md#quick-start-kubernetes--helm--skaffold)
for information on loading test data.

## Example

Our first example, [smeFunc.py](#examples/smeFunc.py), imports our onestop_client package, and passes to it the id, topic, and message handler function. 
Our library then handles the work to connect to kafka and deserialize the message.

1. Here is how to run it in k8s so that the python script can connect to the kafka broker and schema registry:
    ```
    kubectl apply -f examples/pyconsumer-pod.yml
    ```

1. Run this so you can exec the python script within the container:
  
    ```
    kubectl exec -it pyconsumer bash
    ```

1. Then there should be environment variables (you can verify via `echo $OFFSET`) available so you can run this:

    ```
    python ./smeFunc.py -b $KAFKA_BROKERS -s $SCHEMA_REGISTRY -t $TOPIC -g $GROUP_ID -o $OFFSET
    ```

    If not some sensible defaults are in pyconsumer-pod.yml:
    
    ```
    python ./smeFunc.py -b onestop-dev-cp-kafka:9092 -s http://onestop-dev-cp-schema-registry:8081 -t psi-registry-granule-parsed-changelo21`  -g sme-test -o earliest
    ```

    NOTE: 
    If an error prints out of `ERROR    Message handler failed: 'NoneType' object is not subscriptable` that implies the data it was traversing does not have one of the requested values.
    
    Example: If this was in the python script you ran `print(value['fileInformation']['name'])` but the data does not have a value of `fileInformation` it will throw that error.
    
    To fix this you can simply remove ['fileInformation']

## How to publish a new version of this client
>>>>>>> master:python-client/README.md
First you will need to setup your credentials. Create $HOME/.pypirc and update it with the cedardevs username, pw, and token. It will look like the following-
```
[pypi]
  username = __token__
  password = <redacted token>  
```
You'll need a couple tools to create the distribution and then publish it. To install these tools, run the following command-

```
python3 -m pip install --user --upgrade setuptools wheel twine
```
Note: make sure the version on the setup file is changed 

To build the new distribution-
```
python3 setup.py sdist bdist_wheel
```

That should create/update the dist/ directory.

Now to push that to the PyPi repo-

```
python3 -m twine upload dist/*
```

#### Install onestop-python-client-cedardevs package  

```
pip install onestop-python-client-cedardevs
```

importing onestop-python-client-cedardevs package 

producer module have the following functions to import 
    produce: initiate sending a message to Kafka
    list_topics: Request list of topics from cluster
    produce_raw_message: Uses user's inputs to construct a structured input value
    produce_and_publish_raw_collection: raw collection input value and key to initiate sending message to Kafka
    produce_and_publish_raw_granule: raw granule input value and key to initiate sending message to Kafka
    
 ```

from onestop.producer import ... 

```   

consumer module have the following functions to import: 
    consume: consume messages from a given topic 

```

from onestop.consumer import ... 

```   

##Docker
docker build --tag cedardevs/onestop-pyconsumer:latest
docker push cedardevs/onestop-pyconsumer:latest