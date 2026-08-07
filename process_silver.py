import json
import os
import glob
from datetime import datetime

def process_latest_bronze_data():
    bronze_files = glob.glob("bronze/*.json")
    if not bronze_files:
        return
        
    latest_file = max(bronze_files, key=os.path.getctime)
    print(f"Reading raw data from: {latest_file}")
    
    with open(latest_file, "r") as file:
        raw_data = json.load(file)
        
    # NEW: Check if the API actually gave us the 'current' data
    if "current" not in raw_data:
        print(f"Bad API response! Skipping. API said: {raw_data}")
        return
        
    current_data = raw_data["current"]
    
    cleaned_record = {
        "timestamp": current_data.get("time"),
        "pm10_level": current_data.get("pm10"),
        "pm25_level": current_data.get("pm2_5"),
        "location": "Bengaluru"
    }
    
    # NEW: Ensure we actually got a timestamp before saving
    if cleaned_record["timestamp"] is None:
        print("Data is missing a timestamp. Skipping this record.")
        return
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    silver_filename = f"silver/clean_air_{timestamp}.json"
    
    with open(silver_filename, "w") as file:
        json.dump(cleaned_record, file, indent=4)
        
    print(f"Success! Cleaned data saved to {silver_filename}")

if __name__ == "__main__":
    process_latest_bronze_data()