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
        
        # Log the message content
        logger.info("SNS message processed successfully!")
        _LOG.info("SNS message processed successfully!")
    
        
        return {'statusCode': 200,'body': json.dumps('SNS message processed successfully!')}
    

HANDLER = SnsHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
