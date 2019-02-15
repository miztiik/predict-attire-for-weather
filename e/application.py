# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, request
from flask_cors import CORS
from wr_controller import weather_report_controller

app = Flask(__name__, instance_relative_config=True)
CORS(app)

@app.route("/")
def index():
   return render_template('index.html')

@app.route('/get_weather_report', methods=['POST', 'GET'])
def get_weather_report():
    if request.method == 'POST': 
       data = request.json
       input_location = data['location']

       w_report = weather_report_controller()

       geo_location = w_report.getLocation(input_location)
       if geo_location == None:
           wr_address = "Unknown location"
           report_template = render_template('reports.html', weather_address = wr_address)
           return report_template 
       
       wr_address = geo_location.address       
       w_reports = w_report.get_weather_reports(data, geo_location)   

       wr_template = render_template('reports.html', weather_address = wr_address, weather_reports = w_reports)

    return wr_template  

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
