# -*- coding: utf-8 -*-
__author__ = 'Mystique'
"""
.. module: Tag AWS Instances based on common tags in a s3 bucket
    :platform: AWS
    :copyright: (c) 2019 Mystique.,
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

"""
Annual average maximum temperature was 28.96 degree Celsius during 1901. It has increased by 0.26 degree Celsius to 29.22 degree Celsius during 1902 above 1901. We have seen an increase of 0.07 degree Celsius in annual average maximum temperature to 29.16 degree Celsius during 1952 versus 29.09 degree Celsius during 1951. An increase of 0.24 degree Celsius has been observed in annual average maximum temperature from 29.99 degree Celsius during 2001 to 30.23 degree Celsius during 2002. Annual average maximum temperature was 31.42 degree Celsius during 2017, down by -0.21 degree Celsius versus 31.63 degree Celsius during 2016.

The top 5 years in terms of having highest annual average maximum temperature was 2016, 2017, 2009, 2002 and 1995 during the period under consideration. Highest annual average maximum temperature was 31.63 degree Celsius in the year 2016 during the period under consideration, followed by 31.42, 30.3, 30.23 and 30.18 degree Celsius in 2017, 2009, 2002 and 1995 respectively.

The bottom 5 years in terms of having lowest annual average maximum temperature was 1917, 1905, 1909, 1903 and 1950 during the period under consideration. Lowest annual average maximum temperature was 28.11 degree Celsius in the year 1917 during the period under consideration, followed by 28.3, 28.38, 28.47, 28.47 degree Celsius in 1905, 1909, 1903 and 1950 respectively.
"""
import os
import json
import logging
import datetime
from botocore.client import Config
from botocore.client import ClientError

# Initialize Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def set_global_vars() -> dict:
    """
    Set the Global Variables
    If User provides different values, override defaults

    :return: global_vars
    :rtype: dict
    """
    global_vars = {}
    try:
        global_vars['Owner']                = "Mystique"
        global_vars['Environment']          = "Prod"
        global_vars['aws_region']           = "us-east-1"
        global_vars['in_file_name']         = "./data/processed/indian_climate_data.json"
        global_vars['out_file_name']        = "indian_climate_data.json"
        global_vars['status']               = True
    except KeyError as e:
        global_vars['error_message']        = f"Unable to set Global Environment variables. ERROR:{str(e)}."
        global_vars['status']               = False
    return global_vars

################################################
#                                              #
#               HELPER FUNCTIONS               #
#                                              #
################################################

def is_json_valid(data) -> bool:
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

def read_from_file(f):
    """
    Reads the given file handle and returns the data.

    :param f: The file object to be read from
    :param type: file object

    :return data: Returns the file data
    :rtype: dict
    """
    data = False
    # Read the file
    try:
        with open(f) as json_file:
            data = json.load(json_file)
    except Exception as e:
        logger.error(f"Unable to read from file. ERROR:{str(e)}")
    return data

def def write_to_file(data, sort_keys = True, file_name = None):
    """
    Function to write the JSON to file
    """
    time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    o_file_name = '{0}-{1}'.format( time_stamp , file_name )
    o_file_loc = os.path.join( "./", o_file_name )
    with open(o_file_loc, "w") as f:
        json.dump(data, f,indent=2, sort_keys=True, ensure_ascii=False)

def get_avg(l) -> float:
    """
    Python program to get average of a list

    :param l: The list for which avg is to be made
    :param type: list

    :return avg: The avg of the list
    :rtype: decimal
    """
    return ( sum(l) / len(l) )

def wind_dir_names(self):
    return ['North', 'NorthEast', 'East', 'SouthEast', 'South', 'SouthWest', 'West', 'NorthWest']

    #     Name, Lower Limit, Upper Limit, Column, Color
    props = [['Snow', '', 0, 0,  df.sn, 'C7'],
             ['Rain', '', 0, 0, df.rn, 'C2'],
             ['Frigid', '(< -15°C)', -100, -15, df.tmx, 'C1'],
             ['Freezing', '(-15–0)', -15, 0, df.tmx, 'C5'],
             ['Cold', '(0–15)', 0, 15, df.tmx, 'C4'],
             ['Cool', '(15–23)', 15, 23, df.tmx, 'C3'],
             ['Warm', '(23–30)', 23, 30, df.tmx, 'C0'],
             ['Hot', '(≥30)', 30, 100, df.tmx, 'C6']]

def tempAnalysis(temp, HOT, WARM, COOL, COLD, FREEZING):
    if temp >= HOT:
        print("T-Shirt, Shorts")
    
    elif temp <= HOT and temp >= WARM:
        print("T-Shirt and Shorts + Layer")
    
    elif temp <= WARM and temp >= COOL:
        print("Long Pants, Light Jacket")
    
    elif temp <= COOL and temp >= COLD:
        print("Long Pants, Outer Layer and/or Light Jacket")
    
    elif temp <= COLD and temp >= FREEZING:
        print("Long Pants, Winter Jacket, Hat")
    
    elif temp <= FREEZING:
        print("FREEZING: minimize outdoor exposure")

def get_extreme_on_year(data, year: str, get_hot_or_cold: str):
    """
    Find the max temperate for the given year
    
    :param data: The list of climate data
    :param type: list
    :param year: The year for which max is to be found
    :param type: str
    :param get_hot_or_cold: Whether to get the "hottest" or "coldest" month
    :param type: str

    :return: t
    :rtype: float|None
    """
    t = None
    if year in data:
        t = data.get(year).get('extremes').get(get_hot_or_cold +'_temp')
    return t

# top 5 years in terms of having highest annual average maximum
# The top 5 years in terms of having highest annual average maximum temperature was 
# 2016, 2017, 2009, 2002 and 1995 during the period under consideration. Highest annual average maximum temperature was 31.63 degree Celsius in the year 2016 during the period under consideration, followed by 31.42, 30.3, 30.23 and 30.18 degree Celsius in 2017, 2009, 2002 and 1995 respectively.
def get_top_n_hottest(data, n: int, years_or_temps: str):
    """
    Find the top n temperatures
  
    :param data: The list of climate data
    :param type: list
    :param n: The year for which max is to be found
    :param type: str

    :return: 
    :rtype: list
    """
    top_n = {}
    for k in data:
        t = {}
        t[ int( data[k].get('year') ) ] = float( data[k].get('avgs').get('annual').get('max') )
        top_n.update( t )
    # sorted(top_n.values(), reverse=True)
    # sorted(sorted(top_n), key=top_n.get, reverse=True)
    top_n = [(t, top_n[t]) for t in sorted(top_n, key=top_n.get, reverse=True)]
    if years_or_temps == "years": q = 0
    if years_or_temps == "temps": q = 1
    return [x[q] for x in top_n][:n]

def lambda_handler(event, context):
    """
    Entry point for all processing. Load the global_vars

    :return: A dictionary of tagging status
    :rtype: json
    """
    """
    Can Override the global variables using Lambda Environment Parameters
    """
    global_vars = {}
    global_vars = set_global_vars()

    if not global_vars['status']:
        logger.error( global_vars.get('error_message') )
        exit
    
    # ASSUMING MONTH NAMES AND HEADERS ARE LOWER CASE ALREADY

    # Lets begin processing the data
    data = read_from_file( global_vars.get('in_file_name') )

    max_on_year = get_extreme_on_year(data, "1905", "hottest")

    top_n_years = get_top_n_hottest(data, 5, "years")
    top_n_temps = get_top_n_hottest(data, 5, "temps")

    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    

    return max_on_year

if __name__ == '__main__':
    lambda_handler(None, None)