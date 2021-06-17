#!/bin/sh -l

yes | apt update
yes | apt install python3.8
python server.py
