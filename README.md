# Source URL

https://github.com/portikCoder/conti_dckr_py_service

# About the problem:

Was easy to handle, nice little exercise.

# Eye burning elements about my implementation

* as it is kinda demo one, haven't over-engineered as putting in different files the obviously different things
* in-memory with plain RAW sql
* not so much validation of:
    * the inputs
    * and the exception handling

# Solution:

Contains every requirement mentioned in the given pdf file.

## Surplus, without any further validation:

You are able to validate my solution on the fly, here: https://conti-dckr-py-service.herokuapp.com/api/

It is running as dockerized, as it should.

Kindly, the endpoints find here: https://conti-dckr-py-service.herokuapp.com/swagger-ui

# Setup

I won't write down in a very detailed step-by-step install-guide, but instead what I do is, I write a kinda higher
overview.

## For local run, there are some pre-req:

* Have a Python 3.8+ installed
* Have the docker package installed (I was working on a Win machine, but with a Linux subsytem)
    * the easiest way to handle docker is by installing natively on a Unix like machine ;)
* Linux subsystem, or native machine, where Docker is already setup

### If you want to try the app without Dockerization:

* I suggest to create a virtual-environment
* Install the requirements from the file (... -r requirements.txt)

## The interesting part: build & run

* Open the directory of the project
* Build the docker image by: `docker build -t <name-of-your-dockeRrRrrrRr-image-you-want>`
* Run it: `docker run --rm -ti -p 5000:5000 -e PORT=5000 <name-of-your-dockeRrRrrrRr-image-you-want>`
    * or in detached mode: `docker run -d ...`
* Open up your browser/preferred request maker (I am using Postman), and hit there: http://127.0.0.1:5000/swagger-ui

# Usage

For usage checking the previous url shows the right place to do that. Briefly:

* every endpoints can be found on the `/api` path
* to create an entry in the database, use `/api/` with `POST` of an arbitrary element (can be anything you want)
* to get the count for that element you are interested in, make a `GET` with the element (in body)
* to get the average of a specific datatype, request the `/api/avg/<data-type>`
    * there is no type checking if it is a number or not, so in any case (not found or non-existent type) returns **_
      0_** 