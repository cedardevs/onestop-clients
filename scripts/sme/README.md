# SME Script

## AWS Credentials
Populate values for ACCESS_KEY and SECRET_KEY in credentials.yml

## Helm Values
Update values in onestop-sqs-consumer/vaules.yaml. You will want to update the credentials section if you intend to use the mounted helm values. 

## Prerequisites
You will need a kafka broker and a schema-registry running to test this package. To bring up the OneStop stack, see the [OneStop quickstart documentation](https://github.com/cedardevs/onestop/blob/master/docs/developer/quickstart.md#quick-start-kubernetes--helm--skaffold)

### Start up kubernetes clusters using skaffold 

``skaffold dev --status-check=false --force=false``

### Load test data to expose Kafka Topics
```./upload.sh IM COOPS/ localhost/onestop/api/registry```

### Install onestop-python-client repo into directory 

``pip install onestop-python-client``

## Usage

### Upload CSB Data to first topic (psi-granule-input-unknown) 
```python launch_e2e.py -conf config/aws-util-config-dev.yml -cred config/credentials-template.yml```

### Start up sme container
```helm install sme helm/onestop-sqs-consumer```

### Exec into sme container and run extraction code

```kubectl exec -it <name of pod> -- bash```

```python sme.py```


### Look at newly added data in parsed-granule-input topic
```python smeFunc.py```
