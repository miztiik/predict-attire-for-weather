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
        self.get_weather_reportsoption_list = "exclude=currently,minutely,hourly,alerts&units=si"
        """
        if not self.DARK_SKY_API_KEY:
            self.DARK_SKY_API_KEY = "0bdf7cf9b808dec29c52913e70c13f69"
        """
    def getLocation(self, input_location):
        location = Nominatim().geocode(input_location, language='en_US')
        return location
   
    def get_weather_reports(self, data, location):
        """
        Get the weather report for the given location and date
    
        :param data: The JSON data from the form. Ex: {'location': 'Utrecht', 'date_from': '2019-02-14', 'date_to': '2019-02-14'}
        :param type: dict
        :param location: Class Object, Ex: Location(Utrecht, Netherlands, (52.08095165, 5.12768031549829, 0.0))
        :param type: An object of <class 'geopy.location.Location'>
     
        """
        date_from = data['date_from']
        date_to = data['date_to']

        d_from_date = datetime.strptime(date_from , '%Y-%m-%d')
        d_to_date = datetime.strptime(date_to , '%Y-%m-%d')
        delta = d_to_date - d_from_date
        print(f"d_to_date:{d_to_date}")

        latitude = str(location.latitude)
        longitude = str(location.longitude)

        w_reports = []
        for i in range(delta.days+1):
            new_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d')
            search_date = new_date+"T00:00:00"
            # dark_sky_url = f"https://api.darksky.net/forecast/{DARK_SKY_API_KEY}/{latitude},{longitude},{search_date}?{option_list}"
            dark_sky_url = (f"https://api.darksky.net/forecast/"
                            f"{DARK_SKY_API_KEY}/"
                            f"{latitude},"
                            f"{longitude},"
                            f"{search_date}?"
                            f"{self.option_list}"
                            )
            print(dark_sky_url)
            response = requests.get( dark_sky_url )
            json_res = response.json()
            report_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d %A')
            if json_res['flags']['units'] == 'us':
                unit_type = '°F'
            else:
                unit_type = '°C'
            min_temperature = str(json_res['daily']['data'][0]['apparentTemperatureMin']) + unit_type
            max_temperature = str(json_res['daily']['data'][0]['apparentTemperatureMax']) + unit_type
            summary = json_res['daily']['data'][0]['summary']
            icon = json_res['daily']['data'][0]['icon']
            precip_type = None
            precip_prob = None
            raining_chance = None
            if'precipProbability' in json_res['daily']['data'][0] and 'precipType' in json_res['daily']['data'][0]:
                precip_type = json_res['daily']['data'][0]['precipType']
                precip_prob = json_res['daily']['data'][0]['precipProbability']
            if (precip_type == 'rain' and precip_prob != None):
                precip_prob *= 100
                raining_chance = "%.2f%%" % (precip_prob)

            ind_wr = weather_report( report_date,
                                    max_temperature,
                                    min_temperature,
                                    summary,
                                    raining_chance,
                                    icon
                                )        

            w_reports.append(ind_wr)

        return w_reports
