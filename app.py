from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)


WEATHER_API_KEY = '04287418dce27dc13368ed6e6cf14186'  
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

POI_DATA = [
    {'id': 1, 'name': 'British Museum', 'lat': 51.5194, 'lon': -0.1270, 'type': 'history', 'time': 2.5, 'desc': 'Ancient artifacts'},
    {'id': 2, 'name': 'Borough Market', 'lat': 51.5055, 'lon': -0.0910, 'type': 'food', 'time': 1.5, 'desc': 'Local cuisine'},
    {'id': 3, 'name': 'Hyde Park', 'lat': 51.5073, 'lon': -0.1657, 'type': 'nature', 'time': 1.0, 'desc': 'Green space'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    preferences = request.form['preferences'].lower().split(',')
    time_limit = float(request.form['time'])
    lat, lon = float(request.form['lat']), float(request.form['lon'])

    weather = get_weather(lat, lon)
    weather_factor = 0.8 if 'rain' in weather.lower() else 1.0

    itinerary = []
    total_time = 0
    for poi in POI_DATA:
        if any(pref.strip() in poi['type'] for pref in preferences) and total_time + poi['time'] <= time_limit * weather_factor:
            itinerary.append(poi)
            total_time += poi['time']

    points = len(itinerary) * 10 + (10 if weather_factor < 1 else 0)

    return jsonify({
        'itinerary': itinerary,
        'points': points,
        'weather': weather,
        'total_time': total_time
    })

def get_weather(lat, lon):
    try:
        response = requests.get(WEATHER_URL, params={'lat': lat, 'lon': lon, 'appid': WEATHER_API_KEY})
        return response.json()['weather'][0]['description']
    except:
        return 'clear'

if __name__ == '__main__':
    app.run(debug=True)