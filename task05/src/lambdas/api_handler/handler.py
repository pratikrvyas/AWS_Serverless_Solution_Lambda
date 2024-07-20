from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')

import json
import uuid
from datetime import datetime
import boto3


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # try:

        print("1")
        # print(event['Records'])

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('arn:aws:dynamodb:eu-central-1:905418349556:table/cmtr-1bb19304-Events')

        print("2")

        # Generate a unique UUID for the 'id' attribute
        item_id = str(uuid.uuid4())
        
        # Extract the 'content' value from the event
        content = event.get('content')
        
        print("3")
        # Get the current date and time in ISO 8601 format
        created_at = datetime.now().isoformat()
        
        # Create the item to be written to DynamoDB
        item = {
            'id': item_id,
            'principalId': event['principalId'],
            'createdAt': created_at,
            'body': {
                'content': content
            }
        }
        print(item)
        print("4")
        # Write the item to the DynamoDB table
        # table.put_item(Item=item)

        try:
            response = table.put_item(Item=item)
            print(response)
        except Exception as e:
            response = 'Could not process your request: {}'.format(e.response['Error']['Message'])
            print(response)

        # todo implement business logic
        return 200
        # except:
            # print("error")
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
