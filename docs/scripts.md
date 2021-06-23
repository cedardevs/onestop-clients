<div align="center"><a href="/onestop-clients/">Documentation Home</a></div>
<hr>

# Python Scripts for onestop-python-client

## Table of Contents
* [Usage](#usage)
* [Setup](#setup)
    * [Helm](#helm)
    * [Manually Setup Python Environment](#manually-setup-python-environment)
* [Load Data into OneStop](#load-data-into-onestop)
    * [onestop-test-data repository](#onestop-test-data-repositoryhttpsgithubcomcedardevsonestop-test-data)
    * [osim-deployment repository](#osim-deployment-repositoryhttpsgithubcomcedardevsosim-deployment)
* [OneStop Quickstart](https://cedardevs.github.io/onestop/developer/quickstart)

## Usage
Depending on what the script's imports are you may have to install some dependencies via `pip install ...`.
Once ready to execute a script go to the root directory of this project. An example command might be:

`python scripts/sme/sme.py -cred cred.yml`

NOTE:
    * For some scripts you need a credentials file manually and specify the relative location on the command-line via `-cred`
    * The default configuration is set to the location helm will create it, `/etc/config/config.yml`. If you need to specify a different one use the `-conf` command line argument. [Configuration](helm) information is spelled out for helm, since some values you may have to modify if using helm.

## Setup
To use the onestop-python-client there are two options:
* Use our [Helm](helm) charts (Preferred and easiest way)
* Or manually set up your python environment

### Helm
It is recommended to use our helm charts to create the script container. Go [here](helm) for more information.

### Manually Setup Python Environment
* Install conda (miniconda works).
* Restart terminal or source files to recognize conda commands.
* Create a new conda environment and activate it (not convinced you need this)
    * `conda create -n onestop-clients python=3`  
    * `conda activate onestop-clients`
    * `pip install setuptools`

* Install any libraries needed by your script 
    * Ex: `pip install PyYaml`
    
* Install onestop-python-client:
    1. `pip uninstall onestop-python-client-cedardevs`
    1. [Build the onestop-python-client](build-pipeline) if you have modified the code, otherwise it will access the image on github.
    1. `pip install ./onestop-python-client`
    
    To test the import, try this. It shouldn't give an error:
    
    ```
    $ python3
    >>> import onestop_client
    ```

## Load Data into OneStop
There are several repositories to aid in loading data into a OneStop. Please read the appropriate repository's readme for accurate and up to date usage information.

### [onestop-test-data repository](https://github.com/cedardevs/onestop-test-data)
    `./upload.sh demo http://localhost/onestop/api/registry`

### [osim-deployment repository](https://github.com/cedardevs/osim-deployment)
    From the osim-deployment repository there is a staging-scripts directory with scripts for loading some data:
   
    `./copyS3objects.sh -max_files=5 copy-config/archive-testing-demo-csb.sh`
