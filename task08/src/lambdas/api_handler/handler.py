from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json

_LOG = get_logger('ApiHandler-handler')


from lambdas.layers.OpenMeteo_layer.openmeteo.OpenMeteo import OpenMeteo

class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
      
       
   
        # todo implement business logic
        latitude = 52.52  
        longitude = 13.41  
        try:

            print("---1")
            
            weather_data = OpenMeteo.get_weather(latitude, longitude)
            print("---2")
            print(weather_data)
            print("---3")

            # Convert set to dictionary
            # weather_data_final = {str(key): value for key, value in enumerate(weather_data)}

            # return { json.dumps(weather_data_final)}
            return weather_data
        except Exception as e:
            return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

        # return 200
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
