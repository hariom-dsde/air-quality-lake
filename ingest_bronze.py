import requests
import json
from datetime import datetime

def fetch_environmental_data():
    lat, lon = 12.9716, 77.5946
    
    # 1. Fetch Air Quality (Now asking for official US AQI)
    aq_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm10,pm2_5"
    aq_response = requests.get(aq_url).json()
    
    # 2. Fetch Weather (Temperature & Humidity)
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
    weather_response = requests.get(weather_url).json()
    
    # 3. Combine them into one super-record
    combined_data = {
        "raw_timestamp": datetime.now().isoformat(),
        "air_quality": aq_response.get("current", {}),
        "weather": weather_response.get("current", {})
    }
    
    filename = f"bronze/bengaluru_env_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as file:
        json.dump(combined_data, file, indent=4)
        
    print(f"Success! Full weather & AQI data saved to {filename}")

if __name__ == "__main__":
    fetch_environmental_data()