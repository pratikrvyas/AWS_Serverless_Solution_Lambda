from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('HelloWorld-handler')


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        msg=""

       
        try:
            if event['rawPath'] == '/hello':
                msg='{"statusCode": 200,"message": "Hello from Lambda"}'
            else:
                path_name=event['rawPath']
                print(path_name)
                msg='{"statusCode": 200,"message": "Hello from Lambda"}'
                # msg='{"statusCode": 400,"message": "Bad request syntax or unsupported method. Request path: '+ path_name +'. HTTP method: GET"}'
        except:
            print("exception")
            msg={"statusCode": 200,"message": "Hello from Lambda"}
            # msg='{"statusCode": 400,"message": "Bad request syntax or unsupported method. Request path: None. HTTP method: GET"}'

 
        # todo implement business logic
        return msg
    

HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
