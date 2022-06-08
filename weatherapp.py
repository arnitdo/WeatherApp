import json
import tkinter as tk

from requests import request
import requests

from weatherservice import WeatherService

WEATHER_API_KEY = "9a11b75df91e4614988120501220806"

class WeatherApp(tk.Tk):
	def __init__(self, **kwargs):
		super().__init__()
		self.configure(kwargs)
		self.geometry("480x320")
		self.weather_service = WeatherService(WEATHER_API_KEY)

		self.location_search = tk.Entry(self, width = 20)

		self.search_button = tk.Button(self, width = 17, text = "Search", command = self.onSearchClick)

		self.weather_icon_image = tk.PhotoImage()
		self.weather_icon = tk.Label(self, image=self.weather_icon_image)

		self.condition_label = tk.Label(self, text = "", font = ("", 20))

		self.temperature_label = tk.Label(self, text = "", font = ("", 12))
		self.humidity_label = tk.Label(self, text = "", font = ("", 12))

		self.date_labels = []
		self.forecast_images = []
		self.forecast_image_labels = []
		self.forecast_min_temp_labels = []
		self.forecast_max_temp_labels = []
		self.forecast_humidity_labels = []

		self.location_search.grid(row = 0, column = 0, padx = 10)
		self.search_button.grid(row = 1, column = 0, padx = 10)
		self.weather_icon.grid(row = 0, column = 2, rowspan = 2, padx = 10)
		self.condition_label.grid(row = 0, column = 3, rowspan = 2, padx = 10)
		self.temperature_label.grid(row = 3, column = 0, rowspan = 2, columnspan = 2, padx = 10, pady = 20)
		self.humidity_label.grid(row = 3, column = 3, rowspan = 2, columnspan = 2)

		self.loadIPData()
		self.onSearchClick()
		self.mainloop()

	def loadIPData(self):
		city = self.weather_service.getCity()
		self.location_search.insert(0, city)

	def onSearchClick(self):
		location = self.location_search.get()
		if location.strip() == "":
			self.loadIPData()
			self.onSearchClick()
			return
		weather_data = self.weather_service.getDayReport(location)
		forecast_data = self.weather_service.getForecast(location)

		if weather_data["is_day"]:
			image_route = f"weather/64x64/day/{weather_data['image_code']}.png"
		else:
			image_route = f"weather/64x64/night/{weather_data['image_code']}.png"
		
		self.weather_icon_image.config(file = image_route)

		self.condition_label.config(text = weather_data["condition"])
 
		self.temperature_label.config(text = f"Temperature : {weather_data['temperature']}°C")
		self.humidity_label.config(text = f"Humidity : {weather_data['humidity']} millibars")

		for f_date in self.date_labels:
			f_date.destroy()

		for f_image in self.forecast_image_labels:
			f_image.destroy()

		for f_min_t in self.forecast_min_temp_labels:
			f_min_t.destroy()

		for f_max_t in self.forecast_max_temp_labels:
			f_max_t.destroy()

		for f_hum in self.forecast_humidity_labels:
			f_hum.destroy()

		self.date_labels = []
		self.forecast_images = []
		self.forecast_image_labels = []
		self.forecast_min_temp_labels = []
		self.forecast_max_temp_labels = []
		self.forecast_humidity_labels = []

		col_idx = 0
		col_offsets = [0, 2, 3]
		for day_data in forecast_data:
			date = day_data["date"]
			image_route = f"weather/64x64/day/{day_data['image_code']}.png"
			min_temp = day_data['min_temp']
			max_temp = day_data['max_temp']
			humidity = day_data['humidity']

			date_label = tk.Label(self, text = date)

			img = tk.PhotoImage()
			img_label = tk.Label(self, image=img)

			min_t_label = tk.Label(self, text = f"Min : {min_temp}°C")
			max_t_label = tk.Label(self, text = f"Max : {max_temp}°C")
			hum_label   = tk.Label(self, text = f"Hum : {humidity}")

			img.config(file = image_route)
			date_label.grid(row = 5, column = col_offsets[col_idx])
			img_label.grid(row = 6, column = col_offsets[col_idx])
			min_t_label.grid(row = 7, column = col_offsets[col_idx])
			max_t_label.grid(row = 8, column = col_offsets[col_idx])
			hum_label.grid(row = 9, column = col_offsets[col_idx])

			self.date_labels.append(date_label)
			self.forecast_images.append(img)
			self.forecast_images.append(img_label)
			self.forecast_min_temp_labels.append(min_t_label)
			self.forecast_max_temp_labels.append(max_t_label)
			self.forecast_humidity_labels.append(hum_label)

			col_idx += 1