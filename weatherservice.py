import json
import requests

class WeatherService:
	def __init__(self, api_key):
		self.api_key = api_key

	def getCity(self):
		response = requests.get(f"http://api.weatherapi.com/v1/ip.json?key={self.api_key}&q=auto:ip")
		response_json = response.json()
		city = response_json["city"]
		return city

	def getDayReport(self, location):
		response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={location}")
		raw_data = response.json()
		image_code = int(raw_data["current"]["condition"]["icon"][-7:-4])
		json_data = {
			"is_day" : bool(raw_data["current"]["is_day"]),
			"temperature" : raw_data["current"]["temp_c"],
			"humidity" : raw_data["current"]["humidity"],
			"condition" : raw_data["current"]["condition"]["text"],
			"image_code" : image_code
		}
		return json_data

	def getForecast(self, location):
		response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={location}&days=3")
		raw_data = response.json()
		day_forecast = []
		forecast = raw_data["forecast"]["forecastday"]
		for day in forecast:
			day_data = {
				"date" : day["date"]
			}
			day_data.update(day["day"])
			day_forecast.append(day_data)
		processed_day_forecast = []
		for day_data in day_forecast:
			day_json = {
				"date" : day_data["date"],
				"min_temp" : day_data["mintemp_c"],
				"max_temp" : day_data["maxtemp_c"],
				"humidity" : day_data["avghumidity"],
				"image_code" : day_data["condition"]["icon"][-7:-4]
			}
			processed_day_forecast.append(day_json)
		return processed_day_forecast
