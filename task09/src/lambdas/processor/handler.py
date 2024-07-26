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
        table = dynamodb.Table('cmtr-1bb19304-Weather')

        print("--2")

        # Fetch weather data from Open-Meteo API
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")

        print("--3")

        weather_data = response.json()
        weather_data_decimal=  convert_to_decimal(weather_data)

        print("--4")

        # Create a new item in the DynamoDB table
        item = {
            'id': str(uuid.uuid4()),
            'forecast': weather_data_decimal
        }

        
        print("--5")
        try:
            # print(item)
            print("--6")
            table.put_item(Item=item)
        except Exception as e:
            print("--7")
            print(e)
        
        return item
    

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
