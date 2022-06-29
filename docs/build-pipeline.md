<div align="center"><a href="/onestop-clients/">Documentation Home</a></div>
<hr>

# Build Pipeline and Test Execution

## Table of Contents
* [CircleCI](#circleci)
* [Building Manually](#building-manually)
* [Test Execution](#test-execution)

## CircleCI
Currently, this project uses CircleCI to build the multiple images needed. If you example the circleci configuration file you will see what tests it executes and images it builds with what tags.

## Building Manually
* If you change the onestop-python-client code then run this, from the project root:
    
```
docker build . -t cedardevs/onestop-python-client:latest
```

* If you modify just the scripts then run this (only need to do the one relevant for your script), from the project root:
    
```
docker build ./scripts/sqs-to-registry -t cedardevs/onestop-s3-handler:latest
```
    
```
docker build ./scripts/sme/ -t cedardevs/onestop-sme:latest
```

## Test Execution
To execute the onestop-python-client tests via python's unittest execute this from the onestop-python-client directory:

```
python3 -m unittest discover
```

If you wish to run a specific test file, here's an example:

```
python -m unittest test/unit/util/test_S3MessageAdapter.py 
```