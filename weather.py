import requests

API_KEY = "44eea3a795d3596834c164166f544c76"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        rainfall = 0
        if "rain" in data:
            rainfall = data["rain"].get("1h", 0)

        return {
    "temperature": temperature,
    "humidity": humidity,
    "rainfall": rainfall,
    "lat": data["coord"]["lat"],
    "lon": data["coord"]["lon"]
}

    else:
        return None
    
if __name__ == "__main__":
    weather = get_weather("Coimbatore")
    print(weather)