# -*- coding: utf-8 -*-
__author__ = 'Mystique'
"""
.. module: Predict Attire based on weather
    :platform: AWS
    :copyright: (c) 2019 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

from wr_model import weather_report
from geopy.geocoders import Nominatim
from datetime import datetime,timedelta
import requests, json, os, pytz, logging

# Initialize Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class weather_report_controller: 

    def __init__(self):
        self.option_list = "exclude=currently,minutely,hourly,alerts&units=si"
        self.app_config = self.read_from_file( "./configs/prod_config.json" )
        self.DARK_SKY_API_KEY = self.app_config.get('DARK_SKY_API_KEY')
        if not self.DARK_SKY_API_KEY:
            logger.error(f"Unable to read Dark Sky API Configuration")
            return
                
    def is_json_valid(self, data) -> bool:
        """
        This function checks if the given file is a valid json

        :param data: The JSON data to be checked
        :param type: dict

        :return bool: Returns a boolean
        :rtype: bool
        """
        try:
            json.loads( data )
            return True
        except ValueError as error:
            logger.error(f"Invalid JSON data")
            return False

    def read_from_file(self, f):
        """
        Reads the given file handle and returns the data.

        :param f: The file object to be read from
        :param type: file object

        :return data: Returns the file data
        :rtype: dict
        """
        data = None
        # Read the file
        try:
            with open(f) as json_file:
                data = json.load(json_file)
        except Exception as e:
            logger.error(f"Unable to read from file. ERROR:{str(e)}")
        return data

    def get_location(self, input_location):
        """
        Get the lattitude and longitude for the given location

        :param input_location: The name of the location
        :param type: str

        :param location: Class Object, Ex: Location(Utrecht, Netherlands, (52.08095165, 5.12768031549829, 0.0))
        :param type: An object of <class 'geopy.location.Location'>
        """
        location = Nominatim().geocode(input_location, language='en_US')
        return location

    def predict_attire(self, w_r_data, sensitivity_factors):

        # Set some defaults. All numbers in degree celsius
        # TODO: Push them outside for user customizations
        if not sensitivity_factors:
            sensitivity_factors = {'hot':1, 'cold':1}

        WARM = 24 * sensitivity_factors.get('hot')
        COLD = 10 * sensitivity_factors.get('cold')
        HOT = int( WARM + 0.3*(WARM - COLD) )
        COOL = int( (WARM + COLD) / 2 )
        FREEZING = int(COLD - 1*(COOL - COLD))

        attire = {'clothing':'', 'activity':'', 'top_hat':False, 'boots':False, 'coat':False, 'gloves':False, 'scarves':False, 'sunglasses':False, 'umbrella':False, 'stay_indoor':False }
        emoji_dict = {'sunrise':'🌅', 'sunset':'🌇', 't-shirts':'🎽', 'shirts':'👕','neck-tie':'👔','shorts':'\U0001FA73', 'jeans':'👖', 'boots':'👢'}
        if w_r_data.get('raining_chance'):
            attire['umbrella'] = True
            attire['umbrella_emoji'] = f"An ☔ or Rain Jacket, It will 🌧️"
        if w_r_data.get('temp_min') >= HOT:
            attire['clothing'] = f"Minimal Outdoor exposure. Too Hot 🌡️☀️. Stay indoors 🏠🏡 or Stay Cool 🏊🏖️🍹🍨"
            attire['stay_indoor'] = True
        if w_r_data.get('temp_max') >= HOT:
            attire['clothing'] = f"T-Shirts🎽 Shorts\U0001FA73 Sun Glassess🕶 Hat👒 and Shoes👟"
            attire['top_hat'] = True
            attire['sunglasses'] = True
        elif w_r_data.get('temp_max') <= HOT and w_r_data.get('temp_max') >= WARM:
            attire['clothing'] = f"T-Shirts🎽 Shorts\U0001FA73 Sun Glassess🕶 Hat👒 and Shoes👟, Maybe 🍺"
            attire['sunglasses'] = True
        elif w_r_data.get('temp_max') <= WARM and w_r_data.get('temp_max') >= COOL:
            attire['clothing'] = f"Shirts👕 Long Pants👖 Summer Jacket\U0001F9E5 Scarf\U0001F9E3 and Shoes👟, Maybe 🚴"
            attire['scarves'] = True
        elif w_r_data.get('temp_max') <= COOL and w_r_data.get('temp_max') >= COLD:
            attire['clothing'] = f"Shirts👕 Long Pants👖 Light Jacket\U0001F9E5 Gloves\U0001F9E4 Scarf\U0001F9E3 and Boots👢"
            attire['coat'] = True
            attire['gloves'] = True
            attire['scarves'] = True
        elif w_r_data.get('temp_max') <= COLD and w_r_data.get('temp_max') >= FREEZING:
            attire['clothing'] = f"Long sleeved shirt👔👕 Long Pants👖 Winter Jacket\U0001F9E5 Gloves\U0001F9E4 Scarf\U0001F9E3 and Boots👢"
            attire['coat'] = True
            attire['gloves'] = True
            attire['scarves'] = True
            attire['boots'] = True
        elif w_r_data.get('temp_max') <= FREEZING:
            attire['clothing'] = f"Minimal Outdoor exposure 🌡️❄️⛄. Stay indoors 🏠🏡\U0001F525🛌, Stay warm ☕"
            attire['stay_indoor'] = True
        else:
            attire['clothing'] = f"⚡❕❔"

        return attire

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
            w_r_data = { 'temp_min':0,'temp_max':0, 'is_sunny':False, 'will_rain':False }
            new_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d')
            search_date = new_date+"T00:00:00"
            report_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d %A')

            dark_sky_url = (f"https://api.darksky.net/forecast/"
                            f"{self.DARK_SKY_API_KEY}/"
                            f"{latitude},"
                            f"{longitude},"
                            f"{search_date}?"
                            f"{self.option_list}"
                            )
            logger.info(f"DarkSky Request Url: {dark_sky_url}")
            try:
                response = requests.get( dark_sky_url )
            except Exception as err:
                logger.error(f"Unable to fetch data from DarkSky. Error: str{err}")
                return

            wr_data = response.json()
            # Lets break, if we not able to get any data
            if not wr_data.get('daily') or not wr_data.get('daily').get('data'):
                logger.error(f"Unable to fetch data from DarkSky. Response: {wr_data}")
                return

            try:
                # Check if it is for US/Rest of the sensible world and tack on appropriate units
                if wr_data['flags']['units'] == 'us':
                    unit_type = '°F'
                else:
                    unit_type = '°C'

                w_r_data['temp_min'] = wr_data['daily']['data'][0].get('apparentTemperatureMin')
                w_r_data['temp_max'] = wr_data['daily']['data'][0].get('apparentTemperatureMax')
                summary = wr_data['daily']['data'][0].get('summary')

                sunrise = None
                sunset = None
                tz = pytz.timezone(wr_data.get('timezone'))
                if wr_data['daily']['data'][0].get('sunriseTime'):
                    sunrise = datetime.utcfromtimestamp( wr_data['daily']['data'][0].get('sunriseTime') )
                    sunrise = str( pytz.utc.localize(sunrise).astimezone(tz).strftime('%H:%M') )
                if wr_data['daily']['data'][0].get('sunsetTime'):
                    sunset = datetime.utcfromtimestamp( wr_data['daily']['data'][0].get('sunsetTime') )
                    sunset = str( pytz.utc.localize(sunset).astimezone(tz).strftime('%H:%M') )
                humidity = wr_data['daily']['data'][0].get('humidity')
                humidity *= 100
                humidity = "%.0f%%" % (humidity)

                precip_type = None
                precip_prob = None
                w_r_data['raining_chance'] = None
                if 'precipProbability' in wr_data['daily']['data'][0] and 'precipType' in wr_data['daily']['data'][0]:
                    precip_type = wr_data['daily']['data'][0].get('precipType')
                    precip_prob = wr_data['daily']['data'][0].get('precipProbability')
                if (precip_type == 'rain' and precip_prob != None):
                    precip_prob *= 100
                    w_r_data['raining_chance'] = "%.2f%%" % (precip_prob)

                wind_speed = None
                wind_bearing = None
                if 'windSpeed' in wr_data['daily']['data'][0] and wr_data['daily']['data'][0].get('windSpeed') > 0:
                    # WindSpeed is in meters per second, converting to Kmph
                    wind_speed = round( ( wr_data['daily']['data'][0].get('windSpeed') * 3.6) , 2)
                    wind_speed = f"{wind_speed} Kmph"
                    # It is the direction the wind is coming from, so the arrow should be point opposite side, 
                    # or use a inverted image always
                    wind_bearing = wr_data['daily']['data'][0].get('windBearing') + 180

                icon = wr_data['daily']['data'][0].get('icon')
                if wr_data['daily']['data'][0].get('icon') == "clear-day":
                    w_r_data['is_sunny'] = True

                # Lets get the attire predcition
                predicted_attire = self.predict_attire(w_r_data, None)

                # Create a model from the weather report
                # (date, temp_max, temp_min, summary, raining_chance, sunrise, sunset, wind_speed, wind_bearing, humidity, icon, predicted_attire)
                w_report = weather_report( report_date,
                                        str(w_r_data['temp_max']) + unit_type,
                                        str(w_r_data['temp_min']) + unit_type,
                                        summary,
                                        w_r_data['raining_chance'],
                                        sunrise,
                                        sunset,
                                        wind_speed,
                                        wind_bearing,
                                        humidity,
                                        icon,
                                        predicted_attire
                                    )
                # Add the report for current date into the list of reports.
                w_reports.append(w_report)
            except Exception as err:
                logger.error(f"Response data was malformed. Error: str{err}")
                return w_reports

        return w_reports
