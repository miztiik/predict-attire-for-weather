# -*- coding: utf-8 -*-
__author__ = 'Mystique'
"""
.. module: Predict Attire based on weather
    :platform: AWS
    :copyright: (c) 2019 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

from application import application

if __name__ == "__main__":
    application.run()

# gunicorn --bind 0.0.0.0:80 wsgi:application --access-logfile - --error-logfile - &
# "-" redirects the logs to `stdout`

