# Using onestop-python-client

## Table of Contents
* [Setup](#setup)
    * [Helm](#helm)
        * [Use Helm to Create a Script Container](#use-helm-to-create-a-script-container)
        * [Using Helm Config File](#using-helm-config-file)
        * [Helm Pulling of Image](#helm-pulling-of-image)
        * [Startup Helm Script Container](#startup-helm-script-container)
    * [Manually Setup Environment](#manually-setup-environment)
* [Building](#building)
    * [Rebuilding Code or Scripts](#rebuilding-code-or-scripts)
    * [Rebuilding Containers](#rebuilding-containers)
* [Load Data into OneStop](#load-data-into-onestop)
    * [onestop-test-data repository](#onestop-test-data-repositoryhttpsgithubcomcedardevsonestop-test-data)
    * [osim-deployment repository](#osim-deployment-repositoryhttpsgithubcomcedardevsosim-deployment)
* [OneStop Quickstart](https://cedardevs.github.io/onestop/developer/quickstart)
 
## Setup
To use onestop-python-client there are two options: helm or manually.

### Helm
#### Use Helm to Create a Script Container
We use helm to pull a OneStop-Clients image (specified in `helm/<chart directory>/values.yml`) and deploy a kubernetes container that can communicate to the configured OneStop. It also copies over the onestop-python-client and scripts directories to the container.

Those configuration values are in this repo under `helm/<chart directory>/values.yml`. Our helm is configured to create a configuration file in the script container at `/etc/confif/confif.yml` from the appropriate values.yml. You can use this or create your own configuration file and put it in the script container. Our scripts are configured to use the command-line parameter `conf` or will look for the helm configuration file that isn't specified.

#### Using Helm Config File
If you are going to use the helm generated configuration file then you should probably edit the conf section in the helm values.yaml file for the container you will have helm create (Ex. 1helm/onestop-sqs-consumer/values.yaml1).
    * *_metadata_type - should be granule or collection, depending on what you are sending/receiving.
    * schema_registry, registry_base_url, and onestop_base_url - set to what you are communicating with, especially if not on cedar-devs talking to its OneStop.
    * AWS section - there's several config values for AWS you probably need to change, many are set to testing values.
    * Kafka section - There is a whole Kafka section that if you are using kafka you might need to adjust this. This isn't perhaps the most preferred way to submit to OneStop.
    * log_level - If you are troubleshooting or just want to see a more granular log level set this to DEBUG.

#### Helm Pulling of Image
When you run the helm install command helm pulls the specified image from the repository that is indicated in the helm values yaml file.

#### Startup Helm Script Container
The helm install command, done from the root of this repository, will use the charts in the helm directory to create a container called `sme` using the helm charts and configuration information in this repo fom `helm/onestop-sqs-consumer`
    * cd to the root of this repository
    * `helm uninstall sme`
    * `helm install sme helm/onestop-sqs-consumer`

To check on the container run this and look for the pod with the :

`kubectl get pods`
```
(base) ~/repo/onestop-clients 07:00 PM$ kubectl get pods
NAME                                        READY   STATUS    RESTARTS   AGE
sme-onestop-sqs-consumer-5c678675f7-q2s7h   0/1     Pending   0          26s
```
If it isn't in a 'Running' state within 10 seconds then something is probably wrong. If it hasn't crashed yet, CrashBackLoop state, then it is probably a timeout problem trying to connect to a resource.

Once the container is running, which should only be a matter of seconds, you can "ssh" into the container via this command.

NOTE: you need to have the container name listed in the `kubectl get pods` command results for this command:

`kubectl exec --stdin --tty sme-onestop-sqs-consumer-5c678675f7-kmpvn -- /bin/bash`  

### Manually Setup Environment
* Install conda (miniconda works).
* Restart terminal or source files to recognize conda commands.
* Create a new conda environment and activate it (not convinced you need this)
    * `conda create -n onestop-clients python=3`  
    * `conda activate onestop-clients`
    * `pip install setuptools`

* Install any libraries needed by your script 
    * Ex: `pip install PyYaml`
    
    `pip install ./onestop-python-client`
    
    To test the import, try this and it shouldn't give an error:
    
    ```
    $ python3
    >>> import onestop_client
    ```

## Building
Building locally is not necessary if you are using the images that we build automatically. Currently, we build an image via docker files with the tag 'latest' when *any* commits, even branches, are made to github and trigger CircleCI.
You might want to do this is to make code changes, build them, and then run your python script against that pip installed onestop-python-client locally.

### Rebuilding Code or Scripts
* Install the latest onestop-python-client into directory
    
    `pip uninstall onestop-python-client-cedardevs`
    
    `pip install ./onestop-python-client` (run from root of this repository)
   
### Rebuilding Containers
* If the onestop-python-client code changes then run:
    
    `docker build . -t cedardevs/onestop-python-client:latest`

* If just the scripts change
    
    `docker build ./scripts/sqs-to-registry -t cedardevs/onestop-s3-handler`
    
    `docker build ./scripts/sme/ -t cedardevs/onestop-sme:latest`

## Load Data into OneStop
There are several repositories to aid in loading data into a OneStop. Please read the appropriate repository's readme for accurate and up to date usage information.

### [onestop-test-data repository](https://github.com/cedardevs/onestop-test-data)
    `./upload.sh demo http://localhost/onestop/api/registry`

### [osim-deployment repository](https://github.com/cedardevs/osim-deployment)
    From the osim-deployment repository there is a staging-scripts directory with scripts for loading some data:
   
    `./copyS3objects.sh -max_files=5 copy-config/archive-testing-demo-csb.sh`
