from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda


_LOG = get_logger('Processor-handler')

import json
import uuid
import requests
import boto3
from datetime import datetime
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import requests
from decimal import Decimal

class Processor(AbstractLambda):



    def validate_request(self, event) -> dict:
        pass


    
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic

        # Enable X-Ray tracing
        patch_all()
        print("--1")

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('cmtr-1bb19304-Weather-test')

        print("--2")

        # Fetch weather data from Open-Meteo API
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")

        

        weather_data = response.json()
        print("--3")
        print(weather_data)
        print("--4")
        # weather_data_decimal=  convert_to_decimal(weather_data)

        # Transform the data into the desired format
        output_data = {
            "id": str(uuid.uuid4()),  # Generate a new UUID
            "forecast": {
                "elevation": convert_to_decimal(weather_data["elevation"]),
                "generationtime_ms": Decimal(weather_data["generationtime_ms"]),
                "latitude": convert_to_decimal(weather_data["latitude"]),
                "longitude": convert_to_decimal(weather_data["longitude"]),
                "timezone": weather_data["timezone"],
                "timezone_abbreviation": weather_data["timezone_abbreviation"],
                "utc_offset_seconds": convert_to_decimal(weather_data["utc_offset_seconds"]),
                "hourly": {
                    "temperature_2m": convert_to_decimal(weather_data["hourly"]["temperature_2m"]),
                    "time": weather_data["hourly"]["time"]
                },
                "hourly_units": {
                    "temperature_2m": weather_data["hourly_units"]["temperature_2m"],
                    "time": weather_data["hourly_units"]["time"]
                }
            }
        }


        # Print the output data
        print(output_data)

        print("--4")

        # Create a new item in the DynamoDB table
        # item = {
        #     'id': str(uuid.uuid4()),
        #     'forecast': output_data
        # }

        
        print("--5")
        try:
           
            print("--6")
            table.put_item(Item=output_data)
        except Exception as e:
            print("--7")
            print(e)
        
        return output_data
    

HANDLER = Processor()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)

def convert_to_decimal(data):
    """Recursively convert all float values in the data to Decimal."""
    if isinstance(data, dict):
        return {k: convert_to_decimal(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_decimal(i) for i in data]
    elif isinstance(data, float):
        return Decimal(str(data))  # Convert float to Decimal
    return data
