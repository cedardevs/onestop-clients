<div align="center"><a href="/onestop-clients/">Documentation Home</a></div>
<hr>

# OneStop Clients

## Table of Contents
* [Prerequisites](#prerequisites)
* [Credentials](#credentials)
* [Configuration](#configuration)
* [Usage](#usage)
* [How to manually publish a new version of this client](#how-to-manually-publish-a-new-version-of-this-client)

This python package provides an API to connect to OneStop's event stream (aka Inventory Manager). There are several utility modules in the onestop-python-client for posting to Registry or using kafka publishing/consuming to OneStop. There are also some cloud specific utility classes.

## Prerequisites
If you need to bring up the OneStop stack, see the [OneStop quickstart documentation](https://github.com/cedardevs/onestop/blob/master/docs/developer/quickstart.md#quick-start-kubernetes--helm--skaffold)

## Credentials
Copy the `onestop-python-client/config/credentials-template.yml` to a file and fill out the information you will need. If you are using a helm container then copy it to that container.

## Configuration
Here are some configuration values and what they represent. You don't need everything, it depends on what onestop-python-client classes you are using.
If you are using the helm generated configuration file then look in the [helm configuration section](helm#helm-configuration) for what file to modify.

* _metadata_type - should be granule or collection, depending on what you are sending/receiving.
* schema_registry, registry_base_url, and onestop_base_url - set to what you are communicating with, especially if not on cedar-devs talking to its OneStop.
* AWS section - there's several config values for AWS you probably need to change, many are set to testing values.
* Kafka section - There is a whole Kafka section that if you are using kafka you might need to adjust this. This isn't perhaps the most preferred way to submit to OneStop. [OneStop Kafka Topics](https://github.com/cedardevs/onestop/blob/master/kafka-common/src/main/java/org/cedar/onestop/kafka/common/constants/Topics.java) are defined here on how they get named if you do need to listen to a topic. It isn't created until information is published to it (be it via OneStop or these scripts).
* log_level - If you are troubleshooting or just want to see a more granular log level set this to DEBUG.

## Usage
Once you have the OneStop stack (or your own kafka broker + schema registry) running, you are ready to install this package and start consuming messages.

The `onestop_client` can be downloaded via pip, like so-

`python3 -m pip install onestop-python-client-cedardevs`

To test the import, try-

```
$ python3
>>> import onestop_client
```

Look here for more information on executing [scripts](scripts).

## How to manually publish a new version of this client
See the [build pipeline](build-pipeline) for how these images are automatically published.

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
