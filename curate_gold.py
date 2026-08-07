import json, glob, csv

def build_gold_layer():
    silver_files = glob.glob("silver/*.json")
    if not silver_files: return
        
    all_records = []
    for file_path in silver_files:
        with open(file_path, "r") as file:
            record = json.load(file)
            if record.get("timestamp"):
                all_records.append(record)
            
    all_records = sorted(all_records, key=lambda x: x["timestamp"])
    
    gold_filename = "gold/master_air_quality.csv"
    with open(gold_filename, "w", newline='') as csvfile:
        # NEW HEADERS!
        fieldnames = ["timestamp", "location", "temperature_c", "humidity_pct", "official_aqi", "pm10_level", "pm25_level"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(all_records)
        
    print("Success! Master dataset updated with Weather and AQI.")

if __name__ == "__main__":
    build_gold_layer()