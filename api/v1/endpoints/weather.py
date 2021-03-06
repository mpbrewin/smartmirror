from flask_restplus import Resource
from api.v1.restplus import api_ns
from api.v1.parsers import current_weather_parser, hourly_forecast_parser, daily_forecast_parser
import api.v1.http_codes as http_codes
import services.weather

weather_ns = api_ns.namespace('weather', description='Operations related to weather')

@weather_ns.route('/current')
class CurrentWeather(Resource):
	@api_ns.expect(current_weather_parser) #Location (as lat and lon) is optional
	@api_ns.response(200, http_codes._200)
	@api_ns.response(400, http_codes._400)
	@api_ns.response(503, http_codes._503)
	def get(self):
		"""
		Returns the current weather of the region as JSON.

		* Uses openweathermap external API.

		* API Key is hosted server side, and does not need to be provided.

		* The latitude and longitude can be provided as query parameters.

		* Example: 
		```
		smartmirror/weather/current?lat=34.1702&lon=-118.9558
		```

		* If lat and lon are not provided, the API will automatically determine the location of the PI by first calling ```smartmirror/geolocator```
		"""
		response_dict = None
		code = 200

		lat = None; lon = None
		current_weather_args =  current_weather_parser.parse_args()

		#parse location arguments (if present)
		if current_weather_args['lat'] is None or current_weather_args['lon'] is None:
			#lat and lon were not provided, determine location
			location, status = services.geolocator.getLocation()
			if location is None:	#Error
				response_dict = {'status': http_codes._503, 'type': http_codes.EXT_ERR, 'error_message': "Failed to make geolocation request"}
				code = 503
				print(response_dict)
				return response_dict, code
			else:
				lat = location['latitude']
				lon = location['longitude']
		else:
			#lat and lon were provided, parse them
			lat = current_weather_args['lat']
			lon = current_weather_args['lon']

		#weather
		weather, status = services.weather.getCurrentWeather(lat, lon)
		if weather is None:
			response_dict = {'status': http_codes._503, 'type': http_codes.EXT_ERR, 'error_message': "Failed to make weather request"}
			code = 503
			print(response_dict)
		else:
			response_dict = {'status': http_codes._200, 'data':weather}
			
		return response_dict, code


@weather_ns.route('/forecast/hourly')
class HourlyForecast(Resource):
	@api_ns.expect(hourly_forecast_parser) #Location (as state, city) is optional
	@api_ns.response(200, http_codes._200)
	@api_ns.response(400, http_codes._400)
	@api_ns.response(503, http_codes._503)
	def get(self):
		"""
		Returns the hourly weather forecast of the region as JSON.

		* Uses wunderground external API.

		* API Key is hosted server side, and does not need to be provided.

		* The state and city can be provided as query parameters.

		* The state is represented as the region code (e.g. CA for California), and if the city name has spaces, they must be replaced with underscores

		* Example: 
		```
		smartmirror/weather/forecast/hourly?state=CA&city=San_Fransisco
		```

		* If state and city are not provided, the API will automatically determine the location of the PI by first calling ```smartmirror/geolocator```.

		* The JSON returned has 36 entries corresponding to the next 36 hours.
		"""
		response_dict = None
		code = 200

		state = None; city = None
		hourly_forecast_args =  hourly_forecast_parser.parse_args()

		#parse location arguments (if present)
		if hourly_forecast_args['state'] is None or hourly_forecast_args['city'] is None:
			#state and city were not provided, determine location
			location, status = services.geolocator.getLocation()
			if location is None:	#Error
				response_dict = {'status': http_codes._503, 'type': http_codes.EXT_ERR, 'error_message': "Failed to make geolocation request"}
				code = 503
				print(response_dict)
				return response_dict, code
			else:
				state = location['region_code']
				city = location['city']
		else:
			#lat and lon were provided, parse them
			state = hourly_forecast_args['state']
			city = hourly_forecast_args['city']
			city = city.replace(' ', '_') #geolocation returns city name with spaces


		#weather
		weather, status = services.weather.getHourlyForecast(state, city)
		if weather is None:
			response_dict = {'status': http_codes._503, 'type': http_codes.EXT_ERR, 'error_message': "Failed to make hourly forecast request"}
			code = 503
			print(response_dict)
		else:
			response_dict = {'status': http_codes._200, 'data':weather}
			
		return response_dict, code

@weather_ns.route('/forecast/daily')
class DailyForecast(Resource):
	@api_ns.expect(daily_forecast_parser) #Location (as state, city) is optional
	@api_ns.response(200, http_codes._200)
	@api_ns.response(400, http_codes._400)
	@api_ns.response(503, http_codes._503)
	def get(self):
		"""
		Returns the daily weather forecast of the region as JSON.

		* Uses wunderground external API.

		* API Key is hosted server side, and does not need to be provided.

		* The state and city can be provided as query parameters.

		* The state is represented as the region code (e.g. CA for California), and if the city name has spaces, they must be replaced with underscores

		* Example: 
		```
		smartmirror/weather/forecast/daily?state=CA&city=San_Fransisco
		```

		* If state and city are not provided, the API will automatically determine the location of the PI by first calling ```smartmirror/geolocator```

		* The JSON returned has 10 entries corresponding to the next 10 days.
		"""
		response_dict = None
		code = 200

		state = None; city = None
		daily_forecast_args =  daily_forecast_parser.parse_args()

		#parse location arguments (if present)
		if daily_forecast_args['state'] is None or daily_forecast_args['city'] is None:
			#state and city were not provided, determine location
			location, status = services.geolocator.getLocation()
			if location is None:	#Error
				response_dict = {'status': http_codes._503, 'type': http_codes.EXT_ERR, 'error_message': "Failed to make geolocation request"}
				code = 503
				print(response_dict)
				return response_dict, code
			else:
				state = location['region_code']
				city = location['city']
		else:
			#lat and lon were provided, parse them
			state = daily_forecast_args['state']
			city = daily_forecast_args['city']
			city = city.replace(' ', '_') #geolocation returns city name with spaces


		#weather
		weather, status = services.weather.getDailyForecast(state, city)
		if weather is None:
			response_dict = {'status': http_codes._503, 'type': http_codes.EXT_ERR, 'error_message': "Failed to make daily forecast request"}
			code = 503
			print(response_dict)
		else:
			response_dict = {'status': http_codes._200, 'data':weather}
			
		return response_dict, code