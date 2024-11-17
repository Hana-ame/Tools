#!/bin/bash

py blog.py
cd bulletin && git add . && git commit --allow-empty-message -m "" && git push