#!/bin/bash
cd ~/discord_dev
echo "Pulling..."
git pull origin master

echo "Sarting bot..."
python3 run.py
