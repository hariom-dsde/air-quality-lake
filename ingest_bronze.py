import requests
import json
from datetime import datetime

def fetch_air_quality():
    # The base URL without any messy symbols
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    # Using a dictionary prevents copy-paste bugs with special characters
    api_params = {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "current": "pm10,pm2_5"
    }
    
    print("Fetching live data from Open-Meteo...")
    # requests automatically handles formatting the URL safely
    response = requests.get(url, params=api_params)
    data = response.json()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bronze/bengaluru_air_{timestamp}.json"
    
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
        
    print(f"Success! Raw data saved to {filename}")

if __name__ == "__main__":
    fetch_air_quality()