#!/bin/bash

rm -rf lambda.zip;
rm -rf venv-lambda && python3 -m venv venv-lambda && source venv-lambda/bin/activate && pip install . --upgrade && deactivate
cd venv-lambda/lib/python3.6/site-packages/;
zip -ur -D ../../../../lambda.zip mpu;
