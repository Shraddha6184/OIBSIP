import requests

def get_weather_data(location, api_key):
    if location.isdigit():
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={location}&appid={api_key}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch weather data. Status Code: {response.status_code}")
        print("Details:", response.json())
        return None

def display_weather(data):
    if data:
        city = data["name"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_condition = data["weather"][0]["description"]
        print(f"\nWeather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Condition: {weather_condition.capitalize()}")
    else:
        print("No data available to display.")

def main():
    api_key = "6de33e4bb99761da5080e0f8e37c3ded"
    location = input("Enter a city name or ZIP code to get the current weather: ").strip()
    weather_data = get_weather_data(location, api_key)
    display_weather(weather_data)

if __name__ == "__main__":
    main()
