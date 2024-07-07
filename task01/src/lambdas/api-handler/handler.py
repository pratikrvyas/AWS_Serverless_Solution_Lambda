from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        print("7:25 creation")
        str="""
        {
         "statusCode": 200,
         "message": "Hello from Lambda"
        }"""
        dict1={"message" : "Hello from Lambda", "statusCode": 200}
        # dict2={"statusCode": 200}

        # todo implement business logic
        #return 200
        return dict1
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
