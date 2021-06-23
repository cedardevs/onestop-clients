<div align="center"><a href="/onestop-clients/">Documentation Home</a></div>
<hr>

# Helm

## Table of Contents
* [Intro](#intro)
* [Helm Configuration](#helm-configuration)
* [Create and Start the Script Container](#create-and-start-the-script-container)

## Intro
This project has a helm directory which is set up to pull a onestop-python-client image (specified in the image section in `helm/<chart directory>/values.yml`) and create a kubernetes container with that image inside. The container should be able to communicate to the configured OneStop stack (specified in the conf section in `helm/<chart directory>/values.yml`).
 It also copies the onestop-python-client and scripts directories into the container.

## Helm Configuration
The helm charts are setup to create a configuration file from the template at `helm/<chart directory>/values.yml` and copy it to `/etc/config/config.yml` within the container. You don't have to use this file but most likely one will be necessary in a location where the scripts can access it.

Please see the [onestop-python-client configuration](onestop-python-client#configuration) section for configuration information.

Please see the [scripts](scripts) documentation for information on how to pass in a configuration file via CLI and execute the scripts.

## Create and Start the Script Container
The helm install command, done from the root of this repository, will use the charts in the helm directory to create the specified container.
 
In this example we will create the `sme` using the helm charts and configuration information in this repo from `helm/onestop-sqs-consumer`
1. cd to the root of this project
1. `helm uninstall sme`
1. `helm install sme helm/onestop-sqs-consumer`

To check the container status execute `kubectl get pods` and look for the pod with the expected name, as defined by the `name` field in the `helm/<chart directory>/Chart.yaml`:

```
(base) ~/repo/onestop-clients 07:00 PM$ kubectl get pods
NAME                                        READY   STATUS    RESTARTS   AGE
sme-onestop-sqs-consumer-5c678675f7-q2s7h   0/1     Pending   0          26s
```
If it isn't in a 'Running' state within about 10 seconds then something is probably wrong. If it hasn't crashed yet (indicated by a STATUS of CrashBackLoop) then one possibility is a connection timeout trying to connect to a resource.

Once the container is running you can exec into the container (much like "sshing") via this command, use the NAME from the `kubectl get pods` command:

```
kubectl exec --stdin --tty sme-onestop-sqs-consumer-5c678675f7-q2s7h -- /bin/bash
``` 
