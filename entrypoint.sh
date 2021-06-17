#!/bin/sh -l

yes | apt update
yes | apt install python3.8
ip a
python3.8 server.py
