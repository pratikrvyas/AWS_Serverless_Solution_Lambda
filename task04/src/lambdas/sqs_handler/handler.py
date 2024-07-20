from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('SqsHandler-handler')

import json
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SqsHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        
        print("SQS Message")
        # Loop through each record in the event
        for record in event['Records']:
            # The message body is in the 'body' attribute
            message_body = record['body']
            
            try:
                # Log the message content
                logger.info(f"{message_body}")
                _LOG.info(f"{message_body}")
                # Process the message data
                print(f"{message_body}")
            except:
                print(f"Error parsing message: {message_body}")
            
          
            
        return {'statusCode': 200,'body': json.dumps('SQS message processed successfully!')}
    

HANDLER = SqsHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
