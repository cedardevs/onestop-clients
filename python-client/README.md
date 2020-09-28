# OneStop Clients
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

To build the new distribution-
```
python3 setup.py sdist bdist_wheel
```

That should create/update the dist/ directory.

Now to push that to the PyPi repo-

```
python3 -m twine upload dist/*
```

Then you can test it by downloading it

```
pip install onestop-python-client-cedardevs
```
