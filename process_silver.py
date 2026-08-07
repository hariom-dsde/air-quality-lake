import json, os, glob
from datetime import datetime

def process_latest_bronze_data():
    bronze_files = glob.glob("bronze/*.json")
    if not bronze_files: return
        
    latest_file = max(bronze_files, key=os.path.getctime)
    
    with open(latest_file, "r") as file:
        raw_data = json.load(file)
        
    if "air_quality" not in raw_data or "weather" not in raw_data:
        print("Bad API response! Skipping.")
        return
        
    aq = raw_data["air_quality"]
    wx = raw_data["weather"]
    
    cleaned_record = {
        "timestamp": raw_data["raw_timestamp"],
        "location": "Bengaluru",
        "temperature_c": wx.get("temperature_2m"),
        "humidity_pct": wx.get("relative_humidity_2m"),
        "official_aqi": aq.get("us_aqi"),
        "pm10_level": aq.get("pm10"),
        "pm25_level": aq.get("pm2_5")
    }
    
    silver_filename = f"silver/clean_env_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(silver_filename, "w") as file:
        json.dump(cleaned_record, file, indent=4)
    print(f"Success! Silver data saved.")

if __name__ == "__main__":
    process_latest_bronze_data()