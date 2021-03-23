#Scripts

## Table of Contents
* [Quickstart](#quickstart)
* [Kubectl Pod Verification](#kubectl-pod-verification)
* [Load Data](#load-data)
* [Updating Containers](#updating-containers)
 
This directory contains scripts that use the onestop-python-library to send data to a OneStop. 

## Quickstart 
- Install conda (miniconda works).
- Restart terminal or source files to recognize conda commands.
- Create a new conda environment and activate it
  - `conda create -n onestop-clients python=3`  
  - `conda activate onestop-clients`
  - `pip install setuptools`

- Install any libraries needed by your sme script 
  - Ex: `pip install PyYaml`

- Build the latest onestop-python-client
  - `pip uninstall onestop-python-client-cedardevs`
  - `pip install ./onestop-python-client` (run from root of this repository)

- Input credentials for helm in `./helm/onestop-sqs-consumer/values.yaml`
  - Then:
      - `helm uninstall sme`
      - `helm install sme helm/onestop-sqs-consumer`
      
## Kubectl Pod Verification
- Verify onestop-client pod is running, copy the pod name.
  - `kubectl get pods`

- Exec into it
  - `kubectl exec -it <pod name> -- sh` where the <pod name> is listed in `kubectl get pods`

- Check logs
  - `kubectl logs <pod name>`

## Load Data
There are several repositories to aid in loading data into a OneStop. Please read the appropriate repository's readme for accurate and up to date usage information.

- To load data locally you will need a OneStop running locally. This is an example of how to do that, more info in the OneStop repository.
  - `skaffold dev --status-check false`
  
- To load test collections from onestop-test-data repository (read the README for more information) to your local OneStop:
  - `./upload.sh demo http://localhost/onestop/api/registry`
  
- From the osim-deployment repository there is a staging-scripts directory with scripts for loading some data:
  - `./copyS3objects.sh -max_files=5 copy-config/archive-testing-demo-csb.sh`

## Updating Containers
- If the onestop-python-client code changes then run:
  - `docker build . -t cedardevs/onestop-python-client:latest`

- If just the scripts change
  - `docker build ./scripts/sqs-to-registry -t cedardevs/onestop-s3-handler`