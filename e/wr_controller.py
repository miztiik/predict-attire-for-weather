# -*- coding: utf-8 -*-
__author__ = 'Mystique'
"""
.. module: Export Logs from cloudwatch & Store in given S3 Bucket
    :platform: AWS
    :copyright: (c) 2019 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

from wr_model import weather_report
from geopy.geocoders import Nominatim
from datetime import datetime,timedelta
import requests, os

DARK_SKY_API_KEY = os.environ.get('DARK_SKY_KEY')
if not DARK_SKY_API_KEY:
    DARK_SKY_API_KEY = "0bdf7cf9b808dec29c52913e70c13f69"

class weather_report_controller: 

    def __init__(self):
        self.option_list = "exclude=currently,minutely,hourly,alerts&units=si"
        """
        if not self.DARK_SKY_API_KEY:
            self.DARK_SKY_API_KEY = "0bdf7cf9b808dec29c52913e70c13f69"
        """
    def getLocation(self, input_location):
        location = Nominatim().geocode(input_location, language='en_US')
        return location
   
    def get_weather_reports(self, req_data, location):
        """
        Get the weather report for the given location and date
    
        :param data: The JSON data from the form. Ex: {'location': 'Utrecht', 'date_from': '2019-02-14', 'date_to': '2019-02-14'}
        :param type: dict
        :param location: Class Object, Ex: Location(Utrecht, Netherlands, (52.08095165, 5.12768031549829, 0.0))
        :param type: An object of <class 'geopy.location.Location'>
     
        """
        date_from = req_data.get('date_from')
        date_to = req_data.get('date_to')

        d_from_date = datetime.strptime(date_from , '%Y-%m-%d')
        d_to_date = datetime.strptime(date_to , '%Y-%m-%d')
        delta = d_to_date - d_from_date

        latitude = str(location.latitude)
        longitude = str(location.longitude)

        w_reports = []
        for i in range(delta.days+1):
            new_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d')
            search_date = new_date+"T00:00:00"

            dark_sky_url = (f"https://api.darksky.net/forecast/"
                            f"{DARK_SKY_API_KEY}/"
                            f"{latitude},"
                            f"{longitude},"
                            f"{search_date}?"
                            f"{self.option_list}"
                            )

            print(dark_sky_url)
            response = requests.get( dark_sky_url )
            wr_data = response.json()
            report_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d %A')

            # Check if it is for US/Rest of the sensible world and tack on appropriate units
            if wr_data['flags']['units'] == 'us':
                unit_type = '°F'
            else:
                unit_type = '°C'

            min_temperature = str(wr_data['daily']['data'][0]['apparentTemperatureMin']) + unit_type
            max_temperature = str(wr_data['daily']['data'][0]['apparentTemperatureMax']) + unit_type
            summary = wr_data['daily']['data'][0]['summary']
            icon = wr_data['daily']['data'][0]['icon']
            sunrise = str( datetime.fromtimestamp( wr_data['daily']['data'][0]['sunriseTime'] ).strftime('%H:%M') )
            sunset = str( datetime.fromtimestamp( wr_data['daily']['data'][0]['sunsetTime'] ).strftime('%H:%M') )
            humidity = wr_data['daily']['data'][0]['humidity']
            humidity *= 100
            humidity = "%.0f%%" % (humidity)

            precip_type = None
            precip_prob = None
            raining_chance = None

            wind_speed = None
            wind_bearing = None

            if 'precipProbability' in wr_data['daily']['data'][0] and 'precipType' in wr_data['daily']['data'][0]:
                precip_type = wr_data['daily']['data'][0]['precipType']
                precip_prob = wr_data['daily']['data'][0]['precipProbability']
            if (precip_type == 'rain' and precip_prob != None):
                precip_prob *= 100
                raining_chance = "%.2f%%" % (precip_prob)
            if 'windSpeed' in wr_data['daily']['data'][0] and wr_data['daily']['data'][0]['windSpeed'] > 0:
                wind_speed = f"{wr_data['daily']['data'][0]['windSpeed']} Kph"
                wind_bearing = wr_data['daily']['data'][0]['windBearing']

            # Create a model from the weather report
            # (date, max_temperature, min_temperature, summary, raining_chance, sunrise, sunset, wind_speed, wind_bearing, humidity, icon)
            w_report = weather_report( report_date,
                                    max_temperature,
                                    min_temperature,
                                    summary,
                                    raining_chance,
                                    sunrise,
                                    sunset,
                                    wind_speed,
                                    wind_bearing,
                                    humidity,
                                    icon
                                )        
            # Add the report for current date into the list of reports.
            w_reports.append(w_report)

        return w_reports
