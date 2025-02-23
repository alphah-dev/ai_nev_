from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)  # Define app at the top

# OpenWeather API Key (replace with your key)
WEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Mock POI data with types matching user preferences
POI_DATA = [
    {'id': 1, 'name': 'British Museum', 'lat': 51.5194, 'lon': -0.1270, 'type': 'travel', 'time': 2.5, 'desc': 'Ancient artifacts'},
    {'id': 2, 'name': 'Borough Market', 'lat': 51.5055, 'lon': -0.0910, 'type': 'budget', 'time': 1.5, 'desc': 'Local cuisine'},
    {'id': 3, 'name': 'Hyde Park', 'lat': 51.5073, 'lon': -0.1657, 'type': 'language', 'time': 1.0, 'desc': 'Green space'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    print("Form data:", request.form)  # Debug: Log the form data
    preferences = request.form.get('preferences', '').lower().split(',')
    preferences = [p.strip() for p in preferences if p.strip()]  # Clean and filter empty preferences
    print("Parsed preferences:", preferences)  # Debug: Log parsed preferences
    try:
        time_limit = float(request.form['time'])
        lat, lon = float(request.form['lat']), float(request.form['lon'])
    except (KeyError, ValueError) as e:
        print(f"Error parsing form data: {e}")
        return jsonify({'error': 'Invalid input data'}), 400

    # Use preferences directly (no mapping needed since POI types match buttons)
    mapped_preferences = preferences

    # Fetch weather
    weather = get_weather(lat, lon)
    weather_factor = 0.8 if 'rain' in weather.lower() or 'cloud' in weather.lower() else 1.0
    print("Weather:", weather, "Factor:", weather_factor)  # Debug: Log weather

    # Recommend POIs and build itinerary
    itinerary = []
    total_time = 0
    for poi in POI_DATA:
        print(f"Checking POI: {poi['name']}, Type: {poi['type']}")  # Debug: Log each POI check
        if any(pref in poi['type'] for pref in mapped_preferences) and total_time + poi['time'] <= time_limit * weather_factor:
            itinerary.append(poi)
            total_time += poi['time']
            print(f"Added POI: {poi['name']}, New Total Time: {total_time}")  # Debug: Log added POIs

    # Gamification
    points = len(itinerary) * 10 + (10 if weather_factor < 1 else 0)
    print(f"Itinerary: {itinerary}, Points: {points}, Total Time: {total_time}")  # Debug: Log final results

    return jsonify({
        'itinerary': itinerary,
        'points': points,
        'weather': weather,
        'total_time': total_time
    })

def get_weather(lat, lon):
    try:
        response = requests.get(WEATHER_URL, params={'lat': lat, 'lon': lon, 'appid': WEATHER_API_KEY})
        data = response.json()
        print("Weather API response:", data)  # Debug: Log full response
        return data['weather'][0]['description']
    except Exception as e:
        print(f"Weather API error: {e}")
        return 'clear'

if __name__ == '__main__':
    app.run(debug=True)