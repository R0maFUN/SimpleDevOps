#!/bin/sh -l

yes | apt update
yes | apt install python
python server.py
