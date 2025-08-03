import requests
import json
from datetime import datetime
import time
import os

#fetch function
def fetch_and_save():
    url = "https://gbfs.bluebikes.com/gbfs/en/station_status.json"
    response = requests.get(url)
    data = response.json()

    # Timestamp the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"bluebike_data/{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(data, f)

    print(f"Saved snapshot at {timestamp}")

# Create data folder if needed
# Shouldn't be needed, py scripts come in folder called "bluebike_data" which will hold everything
#os.makedirs("bluebike_data1", exist_ok=True)

#fetch station information (e.g. station name, latitude, longitude, etc.)
url = "https://gbfs.bluebikes.com/gbfs/en/station_information.json"
response = requests.get(url)

if response.status_code == 200:
    with open("bluebike_data/station_information.json", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ Downloaded station_information.json")
else:
    print(f"❌ Failed to download. Status code: {response.status_code}")

# Collect data every 5 minutes (adjust as needed)
while True:
    fetch_and_save()
    time.sleep(300)  # 5 minutes