#!/bin/bash

gunicorn --bind 0.0.0.0:8001 predict:app