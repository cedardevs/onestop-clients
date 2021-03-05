# This directory contains scripts that use the onestop-python-library. 

## Quickstart 
- Create a new conda environment and activate it
  conda create -n onestop-clients python=3  
  conda activate onestop-clients
  pip install setuptools

- Install any libraries needed by your sme script 
  pip install PyYaml  

- Build the latest onestop-python-client
  pip uninstall onestop-python-client-cedardevs
  pip install ./onestop-python-client

- Update containers
  If the base library changes build both containers
  docker build . -t cedardevs/onestop-python-client:latest && docker build ./scripts/sqs-to-registry -t cedardevs/onestop-s3-handler

- If just the sme script changes
  docker build ./scripts/sqs-to-registry -t cedardevs/onestop-s3-handler
  
- Update helm values
  Edit/update helm/values.yaml

- Install the sme helm chart  
  helm uninstall sme
  helm install sme helm/onestop-sqs-consumer

- Look for onestop-client pod
  kubectl get pods

- Exec into it
  kubectl exec -it <pod name> -- bash

- Check logs
  kubectl logs <pod name>
  
- Spin onestop locally, from the onestop repo
  skaffold dev --status-check false
  
- Load test collections from onestop-test-data repo
  ./upload.sh demo http://localhost/onestop/api/registry
  
- From the osim-deployment/staging-scripts directory load some data