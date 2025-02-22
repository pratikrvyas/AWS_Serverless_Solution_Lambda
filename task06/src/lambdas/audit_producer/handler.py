from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('AuditProducer-handler')

import json
import boto3
import os
from datetime import datetime
import uuid



class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """

        # Initialize DynamoDB resource
        dynamodb = boto3.resource('dynamodb')

        FLAG_TEST=True

        # Table names can be set in environment variables for flexibility
        CONFIG_TABLE_NAME = "cmtr-1bb19304-Configuration"
        AUDIT_TABLE_NAME = "cmtr-1bb19304-Audit"

        if FLAG_TEST:
            CONFIG_TABLE_NAME = CONFIG_TABLE_NAME + "-test"
            AUDIT_TABLE_NAME = AUDIT_TABLE_NAME + "-test"


        print("1")
        print(FLAG_TEST)
        print(CONFIG_TABLE_NAME)
        print(AUDIT_TABLE_NAME)

        # Reference to the DynamoDB tables
        config_table = dynamodb.Table(CONFIG_TABLE_NAME)
        audit_table = dynamodb.Table(AUDIT_TABLE_NAME)

        print("2")

        for record in event['Records']:
            print(record)

            configuration_key = record['dynamodb']['Keys']['key']['S']
            print(configuration_key)
             

            print(record['eventName'])
            if record['eventName'] == 'MODIFY':
                handle_modify(configuration_key,record,audit_table)
            elif record['eventName'] == 'INSERT':
                handle_insert(configuration_key,record,audit_table)


        return 200
    

def handle_insert(configuration_key,record,audit_table):
    print("3.1")
    new_image = record['dynamodb']['NewImage']
    print(new_image)

    key=new_image["key"]['S']
    value=new_image["value"]['N']

    audit_entry = {
        'id': str(uuid.uuid4()),
        'itemKey': configuration_key,
        'modificationTime': datetime.utcnow().isoformat(),
        "newValue": {"key": key, "value": int(value)}
    }
    save_audit_entry(audit_entry,audit_table)
    

def handle_modify(configuration_key,record,audit_table):
    print("3")
    print(record)
    new_image = record['dynamodb']['NewImage']
    old_image = record['dynamodb']['OldImage']
    print("4")
    for key, value in new_image.items():
        print(key)
        print(value)
        print(new_image[key] )
        print(old_image[key] )
        print(new_image)
        print(old_image)
        if key in old_image and new_image[key] != old_image[key]:
            audit_entry = create_audit_entry(configuration_key, new_image[key], old_image[key])
            save_audit_entry(audit_entry,audit_table)

def create_audit_entry(item_key, new_value, old_value):
    print("5")
    print(item_key)
    print(new_value)
    print(old_value)
    timestamp = datetime.utcnow().isoformat()
    audit_entry = {
        'id': str(uuid.uuid4()),
        'itemKey': item_key,
        'modificationTime': timestamp,
        'updatedAttribute': 'value',
        'oldValue': int(old_value['N']),
        'newValue': int(new_value['N'])
    }
    return audit_entry

def save_audit_entry(audit_entry,audit_table):
    print("6")
    try:
        audit_table.put_item(Item=audit_entry)
        print("7")
        print(f"Audit entry saved: {audit_entry}")
    except Exception as e:
        print(f"Error saving audit entry: {e}")


HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
