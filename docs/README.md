<p align="center">
  <a href="https://cedardevs.github.io/onestop-clients/">
    <img src="images/cedar_devs_logo.png" alt="Cedardevs logo" width="100" height="100">
  </a>
</p>
<h3 align="center">OneStop-clients </h3>

<p align="center">
  onestop commandline interface and subject matter consumer clients 
  <br>
  <a href="https://cedardevs.github.io/onestop/"><strong>Explore OneStop docs »</strong></a>
  <br>
  <br>
  <a href="https://github.com/cedardevs/feedback/issues/new?template=bug.md">Report bug</a>
  ·
  <a href="https://github.com/cedardevs/feedback/issues/new?template=feature.md&labels=feature">Request feature</a>
</p>

## Table of contents
* [onestop-python-client](#onestop-python-client)
* [Python Scripts](#python-scripts)
* [Helm](#helm)
* [CLI](#cli)
* [Build Pipeline and Test Execution](build-pipeline)

This OneStop-clients project is a collection of clients to aid in communicating with OneStop and directly with the cloud.

## [onestop-python-client](onestop-python-client)
The onestop-python-client is a tool for subject matter experts (SME) to publish and consume metadata to and from OneStop as well as directly to the cloud.
This would enable someone to feed data into OneStop, have OneStop digest it, and then read it out via a python script.

[onestop-python-client](onestop-python-client) - More details.

Additional information:
* [onestop-test-data repository readme](https://github.com/cedardevs/onestop-test-data/blob/master/README.md) - loading test data into OneStop.
* [OneStop documentation](https://cedardevs.github.io/onestop/) - OneStop documentation. 

## [Python Scripts](scripts)
There are some sample python scripts that use the onestop-python-client in the scripts directory.

[python scripts](scripts) - More details.

## [Helm](helm)
There is a helm directory full of helm charts to create different kubernetes containers which each contain from this repository the onestop-python-client code and the scripts directory.
 They have python installed so that a SME user could execute scripts from within. 

[Helm](helm) - More details.

## [CLI](cli)
The CLI is an open-sourced commandline interface for OneStop's search API.

* [Developer Quickstart](cli/developer-quickstart)

* [Public User Quickstart](cli/public-user-quickstart)
    
* [SCDR Files](cli/scdr-files)

[CLI](cli) - More details.