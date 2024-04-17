from datetime import datetime
import requests

# Replace with your actual API key
API_KEY = 'SysiBPhRRkBIpkd3I3kHcUmwsGL3fRjx'


def get_weather(city, api_key):
    try:
        api_url = (f'https://api.tomorrow.io/v4/timelines?location={city}&fields=temperature,cloudCover,humidity,'
                   f'precipitationProbability,windSpeed,windDirection&timesteps=1h&units=metric&apikey={api_key}')
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def save_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(data + '\n')


def format_weather_data(weather_data, city_name):
    try:
        # Check the structure of the weather data and extract the required information
        timelines = weather_data.get('data', {}).get('timelines', [])
        if timelines:
            current_weather = timelines[0]['intervals'][0]['values']
            current_time = datetime.now().strftime("%A, %B %d, %Y, %I:%M%p")
            temp_c = current_weather.get('temperature')
            temp_f = temp_c * 9 / 5 + 32
            cloud_cover = current_weather.get('cloudCover')
            humidity = current_weather.get('humidity')
            precipitation_prob = current_weather.get('precipitationProbability')
            wind_speed = current_weather.get('windSpeed')
            wind_direction = current_weather.get('windDirection')
            data = (
                f"Current weather for {city_name} on {current_time}:\n"
                f"Temp in C = {temp_c}\n"
                f"Temp in F = {temp_f}\n"
                f"% Cloud Cover: {cloud_cover}\n"
                f"Humidity: {humidity}\n"
                f"Precipitation Probability: {precipitation_prob}\n"
                f"Wind Direction: {wind_direction}\n"
                f"Wind Speed: {wind_speed}\n"
            )
            return data
        return "Invalid data received from API or incorrect JSON structure."
    except KeyError as e:
        print(f"KeyError: The key {e} was not found in the JSON response.")
        return "There was an error with the JSON structure."


print("ISQA 3900 Weather API")

choice = 'y'
while choice.lower() == 'y':
    city_input = input("Enter City Name: ")
    weather_json = get_weather(city_input, API_KEY)

    if weather_json:
        formatted_data = format_weather_data(weather_json, city_input)
        if formatted_data:
            print(formatted_data)
            output_filename = input("Enter the filename to save the results: ")
            save_to_file(output_filename, formatted_data)

    choice = input("Would you like to enter a new city (y/n): ")

print('Bye')
