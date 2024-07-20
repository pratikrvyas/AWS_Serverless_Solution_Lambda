from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('SnsHandler-handler')

import json
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SnsHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        print("SNS Message")
        # Loop through each record in the event
        for record in event['Records']:
            # Extract the SNS message
            sns_message = record['Sns']['Message']
            
            # If the message is a JSON string, parse it
            try:
                message = json.loads(sns_message)
            except json.JSONDecodeError:
                message = sns_message  # If it's not JSON, keep it as is
            
            # Process the message (for example, print it)
            print("Processed message:", message)
            
            # Log the message content
            logger.info(message)
            _LOG.info(message)
    
        
        return {'statusCode': 200,'body': json.dumps('SNS message processed successfully!')}
    

HANDLER = SnsHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
