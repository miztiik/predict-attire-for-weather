# -*- coding: utf-8 -*-
class weather_report():

    def __init__(self, date, max_temperature,
                min_temperature, summary, raining_chance,
                sunrise, sunset, wind_speed, wind_bearing, humidity,
                icon):
        self.date = date
        self.max_temperature = max_temperature
        self.min_temperature = min_temperature
        self.summary = summary   
        self.raining_chance = raining_chance
        self.sunrise = sunrise
        self.sunset = sunset
        self.wind_speed = wind_speed
        self.wind_bearing = wind_bearing
        self.humidity = humidity
        self.icon = icon