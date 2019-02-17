##################################################################################
## 
## VERSION		:	1.0
## DATE			:	17Feb2019
##
## PURPOSE      :   Recommend attire based on weather
## USAGE		:	
### Build       :   docker build --tag="predict-attire-for-weather" .
### Run         :   docker run -dti -p 80:80 --name attire_recommender predict-attire-for-weather
##################################################################################

FROM python:3.7.2-alpine3.9
LABEL maintainer="https://github.com/miztiik"

# Install the application libraries
RUN pip install flask flask-cors requests geopy pytz gunicorn

# Lets copy the app source code to the container image
COPY ./src /var/predict-attire-for-weather

# Set the workdirectory to make it easy for testing
WORKDIR /var/predict-attire-for-weather

# Set the entry point to start the gunicorn applicaiton server
# Sample cmd - `gunicorn --bind 0.0.0.0:80 wsgi:application --access-logfile - --error-logfile -`
EXPOSE 80
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "wsgi:application", "--access-logfile", "-", "--error-logfile", "-"]