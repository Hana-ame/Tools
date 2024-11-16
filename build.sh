#!/bin/bash

py blog.py
cd bulletin && git add . && git commit -m "build.sh" && git push