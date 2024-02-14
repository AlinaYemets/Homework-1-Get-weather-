import datetime as dt
import json
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_TOKEN = ""
RSA_KEY = ""

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv

def generate_weather(location, date):
    url_base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    url = f"{url_base_url}/{location}/{date}?unitGroup=metric&include=days&key={RSA_KEY}&contentType=json"
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else: 
        raise InvalidUsage(response.text, status_code=response.status_code)

def valid_name(name):
    parts = name.split()
    if len(parts) != 2:
        return False
    for part in parts:
        if not part.isalpha():
            return False
    return True

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/")
def home_page():
    return "<p><h2>KMA Homework1</h2></p>"

@app.route("/weather", methods=["POST"])
def weather_endpoint():
    json_data = request.get_json()

    token = json_data.get("token")
    requester_name = json_data.get("requester_name")
    location = json_data.get("location")
    date = json_data.get("date")

    if requester_name is None:
        raise InvalidUsage("name is required", status_code=400)
    if location is None:
        raise InvalidUsage("location is required", status_code=400)
    if date is None:
        raise InvalidUsage("date is required", status_code=400)
    if token is None:
        raise InvalidUsage("token is required", status_code=400)
    if not valid_name(requester_name):
        raise InvalidUsage("unvalid name", status_code=400)    
    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    weather_data = generate_weather(location, date)['days'][0]
    
    result = {
        "requester_name": requester_name,
        "timestamp": dt.datetime.utcnow().isoformat() + "Z",
        "location": location,
        "date": date,
        "weather": 
                   {
                    "temp_c": weather_data['temp'],
                    "temp_feelslike_c": weather_data['feelslike'],
                    "wind_kph": weather_data['windspeed'],
                    "pressure_mb": weather_data['pressure'],
                    "humidity": weather_data['humidity'],
                    "snow_cm": weather_data['snow']
                   }
    }

    return result

