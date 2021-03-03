# This directory contains scripts that use the onestop-python-library. 

## Quickstart 
- Create a new conda environment and activate it
  conda create -n onestop-clients python=3  
  conda activate onestop-clients
  pip install setuptools

- Install any libraries needed by your sme script 
  pip install PyYaml  

- Build the latest onestop-python-client
  pip install ./onestop-python-client

- Update containers
  docker build . -t cedardevs/onestop-python-client:latest && docker build ./scripts/sqs-to-registry/ -t cedardevs/onestop-sme:latest

- Update helm values
Edit/update helm/values.yaml

- Install the sme helm chart  
helm install sme helm/onestop-sqs-consumer

- Look for onestop-client pod
kubectl get pods

- Exec into it
kubectl exec -it <pod name> -- bash

- Run your sme script when testing locally
python <sme_script>.py -cmd consume -b onestop-dev-cp-kafka:9092 -s http://onestop-dev-cp-schema-registry:8081 -t psi-granule-input-unknown -g sme-test -o earliest