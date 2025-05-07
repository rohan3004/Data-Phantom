#!/bin/bash

cd /home/ubuntu/Data-Phantom
source /home/ubuntu/Data-Phantom/venv/bin/activate
python /home/ubuntu/Data-Phantom/scrape.py >> cron.log 2>&1
