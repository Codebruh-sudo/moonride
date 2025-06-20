#setup 
#! /bin/bash

# clone
git clone https://github.com/YOUR_USERNAME/MOONRIDE.git
cd contact-deduplication-api

# install dependencies
pip install -r requirement.txt

# run locally
python task.py

# test
python test_shadow.py
