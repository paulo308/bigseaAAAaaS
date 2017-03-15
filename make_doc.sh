#!/bin/bash

# build the documentation
sudo python setup.py install
cd docs/source/
make clean
make html
