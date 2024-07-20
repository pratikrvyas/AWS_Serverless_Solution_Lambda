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
        # table = dynamodb.Table('arn:aws:dynamodb:eu-central-1:905418349556:table/cmtr-1bb19304-Events')
        table = dynamodb.Table('cmtr-1bb19304-Events-test')

        print("2")

        # Generate a unique UUID for the 'id' attribute
        item_id = str(uuid.uuid4())
        
        # Extract the 'content' value from the event
        content = event.get('content')
        
        print("3")
        # Get the current date and time in ISO 8601 format
        created_at = datetime.now().isoformat()
        
        # Create the item to be written to DynamoDB
        # item_1 = {
        #     'id': item_id,
        #     'principalId': event['principalId'],
        #     'createdAt': created_at,
        #     'body':  content
            
        # }

        # item={
        #         "id":  item_id,
        #         "principalId": {"N": event['principalId']},
        #         "createdAt": {"S": created_at},
        #         "body": {"M": {"content": content}}
        #         }

        item = {
            'id': item_id,
            'principalId': int(event['principalId']),
            'createdAt': created_at,
            'body':  dict(map(lambda item: (item[0], item[1]), content.items()))
            
        }
        print(item)
       
        print("4")
        # Write the item to the DynamoDB table
        # table.put_item(Item=item)

        try:
            print("5")
            response=table.put_item(Item=item)
            print(response)
            print("6")
            
        except Exception as e:
            print("7")
            print(e)
           

        # todo implement business logic
        
        return {"statusCode": 201,"event": item }
        
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
