import requests
import json
import os
from datetime import datetime

DATA_FILE = "data.json"
latest_data = None

def get_current_time():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")

def weather():
    global latest_data
    city = input("\nEnter city name: ").strip()
    if not city:
        print("Error: City name cannot be empty!")
        return
    print(f"\nFetching weather data for '{city}'...")
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        weather_info = {
            "type": "weather",
            "city": city.title(),
            "temperature": int(current["temp_C"]),
            "humidity": int(current["humidity"]),
            "wind_speed": int(current["windspeedKmph"]),
            "condition": current["weatherDesc"][0]["value"],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        latest_data = weather_info
        print("\n" + "=" * 30)
        print("------ Weather Report ------")
        print(f"City:        {weather_info['city']}")
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Humidity:    {weather_info['humidity']}%")
        print(f"Wind Speed:  {weather_info['wind_speed']} km/h")
        print(f"Condition:   {weather_info['condition']}")
        print(f"Fetched At:  {get_current_time()}")
        print("=" * 30)
    except requests.exceptions.RequestException as e:
        print(f"\nError: Failed to fetch weather data. ({e})")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"\nError: Could not parse weather data. ({e})")

def currency():
    global latest_data
    base = input("\nBase Currency (e.g., USD): ").strip().upper()
    target = input("Target Currency (e.g., BDT): ").strip().upper()
    if not base or not target:
        print("Error: Both currencies are required!")
        return
    if base == target:
        print("Error: Base and target cannot be the same!")
        return
    print(f"\nFetching exchange rate: {base} -> {target}...")
    try:
        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("result") != "success":
            print(f"\nError: API returned error for '{base}'.")
            return
        rates = data.get("rates", {})
        if target not in rates:
            print(f"\nError: Currency '{target}' not found.")
            return
        rate = rates[target]
        currency_info = {
            "type": "currency",
            "base": base,
            "target": target,
            "rate": round(rate, 2),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        latest_data = currency_info
        print("\n" + "=" * 30)
        print("----- Currency Exchange -----")
        print(f"1 {base} = {rate:.2f} {target}")
        print(f"Fetched At: {get_current_time()}")
        print("=" * 30)
    except requests.exceptions.RequestException as e:
        print(f"\nError: Failed to fetch currency data. ({e})")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"\nError: Could not parse currency data. ({e})")

def save_json():
    global latest_data
    if latest_data is None:
        print("\nError: No data to save! Fetch data first.")
        return
    try:
        existing_data = []
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
            except (json.JSONDecodeError, IOError):
                existing_data = []
        existing_data.append(latest_data)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        print(f"\nSuccess! Data saved to '{DATA_FILE}'.")
    except PermissionError:
        print(f"\nError: Cannot write to '{DATA_FILE}'.")
    except Exception as e:
        print(f"\nError: Failed to save data. ({e})")

def view_json():
    if not os.path.exists(DATA_FILE):
        print(f"\nNo saved data found. '{DATA_FILE}' does not exist.")
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data:
            print("\nThe data file is empty.")
            return
        if isinstance(data, dict):
            data = [data]
        print(f"\n{'=' * 40}")
        print("         Previous Saved Data")
        print(f"{'=' * 40}")
        for i, record in enumerate(data, 1):
            print(f"\n--- Record #{i} ---")
            if record.get("type") == "weather":
                print(f"Type:        Weather")
                print(f"City:        {record.get('city', 'N/A')}")
                print(f"Temperature: {record.get('temperature', 'N/A')}°C")
                print(f"Humidity:    {record.get('humidity', 'N/A')}%")
                print(f"Wind Speed:  {record.get('wind_speed', 'N/A')} km/h")
                print(f"Condition:   {record.get('condition', 'N/A')}")
                print(f"Saved Time:  {record.get('time', 'N/A')}")
            elif record.get("type") == "currency":
                print(f"Type:        Currency Exchange")
                print(f"Base:        {record.get('base', 'N/A')}")
                print(f"Target:      {record.get('target', 'N/A')}")
                print(f"Rate:        1 {record.get('base', '')} = {record.get('rate', 'N/A')} {record.get('target', '')}")
                print(f"Saved Time:  {record.get('time', 'N/A')}")
        print(f"\n{'=' * 40}")
        print(f"Total Records: {len(data)}")
        print(f"{'=' * 40}")
    except json.JSONDecodeError:
        print(f"\nError: '{DATA_FILE}' has invalid JSON.")
    except Exception as e:
        print(f"\nError: Failed to read data. ({e})")

def main_menu():
    while True:
        print("\n" + "=" * 30)
        print("      = Data Fetcher =")
        print("=" * 30)
        print("1. Current Weather")
        print("2. Currency Exchange Rate")
        print("3. Save Result to JSON File")
        print("4. View Previous Saved Data")
        print("5. Exit")
        print("=" * 30)
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            weather()
        elif choice == "2":
            currency()
        elif choice == "3":
            save_json()
        elif choice == "4":
            view_json()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice! Enter 1-5.")

if __name__ == "__main__":
    main_menu()