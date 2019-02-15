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
        global_vars['in_file_name']         = "./source/seasonal-and-annual-minmax-temp-series-india-1901-2017-v0.1.json"
        global_vars['out_file_name']        = "indian_climate_data.json"
        global_vars['status']               = True
    except KeyError as e:
        global_vars['error_message']        = f"Unable to set Global Environment variables. ERROR:{str(e)}."
        global_vars['status']               = False
    return global_vars

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

def get_avg(l) -> float:
    """
    Python program to get average of a list

    :param : The list for which avg is to be made
    :param type: list

    :return avg: The avg of the list
    :rtype: decimal
    """
    return ( sum(l) / len(l) )

def write_to_file(data, sort_keys = True, file_name = None):
    """
    Function to write the JSON to file
    """
    time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    o_file_name = '{0}-{1}'.format( time_stamp , file_name )
    o_file_loc = os.path.join( "./", o_file_name )
    with open(o_file_loc, "w") as f:
        json.dump(data, f,indent=2, sort_keys=True, ensure_ascii=False)

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

    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    
    # Movings months to its own key
    for i in data:
        monthly_avg = {}
        for j in months:
            monthly_avg[j] = i[j]
            i.pop(j, None)
        i['monthly_avg'] = monthly_avg
    
    n_data = {}

    for enum, i in enumerate(data):
        # Find & Add, Hottest & Coldest Months per year
        i['extremes'] = {}
        i['extremes']['hottest_month'] = max(i['monthly_avg'], key=i['monthly_avg'].get)
        i['extremes']['hottest_temp'] = i['monthly_avg'][ i['extremes']['hottest_month'] ]
        i['extremes']['coldest_month'] = min(i['monthly_avg'], key=i['monthly_avg'].get)
        i['extremes']['coldest_temp'] = i['monthly_avg'][ i['extremes']['coldest_month'] ]

        # Lets try to get yearly average
        a = i.get('monthly_avg').values()
        a = [float(x) for x in a]
        i['annual_avg'] = str( round(get_avg(a),2) )

        # Repackage "averages"
        # Rename the "annual_max" to "annual_avg_of_max" & "annual_min" to "annual_avg_of_min"
        i['avgs'] = {'annual':{},'seasonal':{}, 'monthly':{}}
        i['avgs']['annual']['avg'] = i.pop('annual_avg', None)
        i['avgs']['annual']['max'] = i.pop('annual_max', None)
        i['avgs']['annual']['min'] = i.pop('annual_min', None)

        # Seasonal Averages
        i['avgs']['seasonal']['jan_feb_max'] = i.pop('jan_feb_max', None)
        i['avgs']['seasonal']['jan_feb_min'] = i.pop('jan_feb_min', None)
        i['avgs']['seasonal']['jun_sep_max'] = i.pop('jun_sep_max', None)
        i['avgs']['seasonal']['jun_sep_min'] = i.pop('jun_sep_min', None)
        i['avgs']['seasonal']['mar_may_max'] = i.pop('mar_may_max', None)
        i['avgs']['seasonal']['mar_may_min'] = i.pop('mar_may_min', None)
        i['avgs']['seasonal']['oct_dec_max'] = i.pop('oct_dec_max', None)
        i['avgs']['seasonal']['oct_dec_min'] = i.pop('oct_dec_min', None)

        # Monthly Averages
        i['avgs']['monthly'] = i.pop('monthly_avg', None)



        # Repackage the data as dictionary, with year as key
        n_data[i['year']] = i

    write_to_file(n_data, sort_keys = False, file_name = global_vars.get('out_file_name'))

    return data

if __name__ == '__main__':
    lambda_handler(None, None)