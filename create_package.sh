#!/bin/bash

rm -rf lambda.zip;
rm -rf venv-lambda && python3.6 -m venv venv-lambda --without-pip && source venv-lambda/bin/activate && curl https://bootstrap.pypa.io/get-pip.py | python && pip install . && deactivate
cd venv-lambda/lib/python3.6/site-packages/;
zip -ur -D ../../../../lambda.zip mpu;
