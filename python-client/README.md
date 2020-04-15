#OneStop Clients

This python package provides an API to connect to OneStop's event stream (aka Inventory Manager). At this early stage there is only a single module for consuming messages from the kafka brokers that back OneStop.

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
`kubectl apply -f examples/pyconsumer-pod.yml`

At the moment, that pod will tail -f /dev/null to stay open so you can exec into the container with -
`kubectl exec -it pyconsumer bash`

And then there should be env vars available so you can run this -
`python ./smeFunc.py -b $KAFKA_BROKERS -s $SCHEMA_REGISTRY -t $TOPIC -g $GROUP_ID`

or adjust it as needed.
