from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json

_LOG = get_logger('HelloWorld-handler')


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        dict1={"message" : "Hello from Lambda", "statusCode": 200}
        print("hi 8-July at 7:40 pm")
        # todo implement business logic
        # return {
        #     "statusCode" : 200,
        #     "message" : json.dump("Hello from Lambda")
        # }
        return '{"statusCode": 200, "message": "Hello from Lambda"}'
    

HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
