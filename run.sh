#!/bin/bash

# Define variables
NUM_WORKERS=4
BIND_ADDRESS="0.0.0.0:5000"
APP_MODULE="app:app"
CONFIG_FILE="gunicorn_config.py"

# Run Gunicorn
gunicorn -w $NUM_WORKERS -b $BIND_ADDRESS -c $CONFIG_FILE $APP_MODULE