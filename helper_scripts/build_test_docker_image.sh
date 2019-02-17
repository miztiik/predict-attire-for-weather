#!/bin/bash
set -x
set -e

# Prepare dev/container environment for building image
cd /var

## Install git client
yum -y install git

## Lets get the application code
git clone https://github.com/miztiik/predict-attire-for-weather.git && \
cd /var/predict-attire-for-weather

## Build the container image

### Build
docker build --tag="predict-attire-for-weather" .

### Test the new image
docker run -dti -p 80:80 --name attire_recommender predict-attire-for-weather

### Clean Up
docker stop attire_recommender;docker rm attire_recommender; docker rmi mystique/predict-attire-for-weather

### Run Image from DockerHub
docker run -dti -p 80:80 --name attire_recommender mystique/predict-attire-for-weather