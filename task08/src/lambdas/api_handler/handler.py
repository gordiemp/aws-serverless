import json

import requests
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


import asyncio

# from open_meteo import OpenMeteo
# from open_meteo.models import DailyParameters, HourlyParameters


def remove_none_values(d):
    if not isinstance(d, dict):
        return d
    return {k: remove_none_values(v) for k, v in d.items() if v is not None}


class MeteoForecast:

    def get_weather_forecast(self):
        url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=' \
              'temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'
        response = requests.get(url)

        return response.json()


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        if 'rawPath' in event:
            print(f'rawPath: {event["rawPath"]}')
        mf = MeteoForecast()
        forecast = mf.get_weather_forecast()
        # forecast = remove_none_values(forecast)

        print(forecast)
        return forecast


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
