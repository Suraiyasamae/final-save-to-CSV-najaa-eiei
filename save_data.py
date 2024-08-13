import requests
import csv
from datetime import datetime

ESP32_IP = "192.168.0.14"  # Replace with your ESP32's IP address
URL = f"http://{ESP32_IP}/save"

def get_thermal_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_csv(data, filename="thermal_data.csv"):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + data)

# Main execution
data = get_thermal_data()
if data:
    save_to_csv(data)
    print("Data saved to CSV")
else:
    print("Failed to get data")