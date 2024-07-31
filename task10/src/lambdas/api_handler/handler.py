from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


import json
import boto3
import uuid
import re
from botocore.exceptions import ClientError





class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic

        # Initialize AWS services
        try:

            cognito_client = boto3.client('cognito-idp')
            dynamodb = boto3.resource('dynamodb')

            tables_table = dynamodb.Table('cmtr-1bb19304-Tables')
            reservations_table = dynamodb.Table('cmtr-1bb19304-Reservations')
            USER_POOL_NAME="cmtr-1bb19304-simple-booking-userpool"
            
            FLG_TEST=True

            if FLG_TEST:
                 tables_table = dynamodb.Table('cmtr-1bb19304-Tables-test')
                 reservations_table = dynamodb.Table('cmtr-1bb19304-Reservations-test')
                 USER_POOL_NAME="cmtr-1bb19304-simple-booking-userpool-test"



            print("----start-----")
            print("Received event:", json.dumps(event))

            route=event['path']
            cognito_client = boto3.client('cognito-idp')
            response = cognito_client.list_user_pools(MaxResults=60) 

            # booking-userpool: simple-booking-userpool


            for pool in response['UserPools']:
                # print(f"User Pool ID: {pool['Id']}, Name: {pool['Name']}")
                if pool['Name']==USER_POOL_NAME:
                    my_pool=pool
               

            print("--mypool--")
            print(my_pool['Name']) 
            print(my_pool['Id'])

            USER_POOL_ID = str(my_pool['Id'])
            print(USER_POOL_ID)
            response = cognito_client.list_user_pool_clients( UserPoolId=USER_POOL_ID)
            CLIENT_ID = response['UserPoolClients'][0]['ClientId']
            print("---client id")
            print(CLIENT_ID)

            print(route)

           

            if route == '/signup':
                print("---1")
                return signup(event,USER_POOL_ID,cognito_client)
            elif route == '/signin':
                print("---2")
                return signin(event,USER_POOL_ID,CLIENT_ID,cognito_client)
            elif event['path'].startswith('/tables/') and event['httpMethod']  == 'GET':

                # if len(event['path'].split('/')) < 3:
                #     return {
                #         'statusCode': 400,
                #         'body': json.dumps({'error': 'Invalid URL format.'})
                #     }
                print("---get table with id---")
                print(event['path'])
                table_id = event['path'].split('/')[-1]
                return get_table_with_id(event,tables_table,table_id)

            elif route == '/tables':
                print("---3")
                if event['httpMethod'] == 'POST':
                    print("---3")
                    return create_table(event,tables_table)
                elif  event['httpMethod'] == 'GET':
                    print("----6---")
                    path = event['path']
                    # print(path)
                    # path_segments = path.split('/')
                    # if len(path_segments) == 3:
                    #     print("---6.1")
                    #     # Extract the tableId from the route
                    #     print(route)
                    #     table_id = route.split('/')[-1]  # Get the last segment of the path
                        
                    #     print(f"Fetching details for tableId: {table_id}")
                    #     return get_table_with_id( event,tables_table,table_id)
                    # else:
                    print("---6.2")
                    return get_tables(event,tables_table)
            elif route == '/reservations':
                if event['httpMethod'] == 'POST':
                    print("---7")
                    return create_reservation(event,reservations_table,tables_table)
                elif  event['httpMethod'] == 'GET':
                    print("---8")
                    return get_reservations(event,reservations_table)
            
           
            print("---10---")

           
        except Exception as e:
            print("----error")    
            print(e)
            return 401


       



       
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)


def signup(event,USER_POOL_ID,cognito_client):

    print("---1-start")
    body = json.loads(event['body'])
    email = body['email']
    password = body['password']
    
    # Validate email and password
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {'statusCode': 400, 'body': json.dumps('Invalid email')}
    if len(password) < 12 or not re.search(r"[A-Za-z0-9$%^*]", password):
        return {'statusCode': 400, 'body': json.dumps('Invalid password')}
    
    try:
        print(USER_POOL_ID)
        print(email)
        print(password)
        response = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
            ],
            MessageAction='SUPPRESS'  # Prevent sending a verification email
        )
        cognito_client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=email,
            Password=password,
            Permanent=True
        )
        print("---1-end")
        return {'statusCode': 200, 'body': json.dumps('Sign-up successful')}
    except ClientError as e:
        print("--error--")
        print(e)
        # return {'statusCode': 400, 'body': json.dumps(str(e))}

def signin(event,USER_POOL_ID,CLIENT_ID,cognito_client):

    print("---2-signin-start")
    body = json.loads(event['body'])
    email = body['email']
    password = body['password']
    
    try:
        response = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
            }
        )
    
        access_token = response['AuthenticationResult']['IdToken']
                       

        print("---2-signin--end")
        return {'statusCode': 200, 'body': json.dumps({'accessToken': access_token})}
    except ClientError as e:
        return {'statusCode': 400, 'body': json.dumps(str(e))}

from decimal import Decimal
def convert_decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Type not serializable")

def get_tables(event,tables_table):
    print("---3-get_tables--start")

    # Fetch tables from DynamoDB
    response = tables_table.scan()
   
    print(response)
    # item=convert_decimal_to_float(response['Items'])
    print("---3-get_tables--end")
    # return response['Items']
    return {'statusCode': 200, 'body': json.dumps({'tables': response['Items'] }, default=convert_decimal_to_float)}
    # return {'statusCode': 200, 'body': json.dumps({'tables': item})}

def create_table(event,tables_table):
    body = json.loads(event['body'])
    
  
    print("---4-create_table--start")
    # Create a new table entry
    item = {
        'id': int(body['id']),
        'number': body['number'],
        'places': body['places'],
        'isVip': body['isVip'],
        'minOrder': body.get('minOrder', None)
    }
    
    tables_table.put_item(Item=item)
    print("---4-create_table--end")
    return {'statusCode': 200, 'body': json.dumps({'id': body['id']})}


def serialize_item(item):
    """Convert DynamoDB item to a JSON serializable format."""
    if isinstance(item, dict):
        return {k: serialize_item(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [serialize_item(i) for i in item]
    elif isinstance(item, Decimal):
        return float(item)  # Convert Decimal to float
    else:
        return item  # Return the item as is if it's already serializable

def get_table_with_id(event,tables_table,table_id):

    # Extract tableId from the path
    # table_id = event['pathParameters']['tableId']
    
    # Fetch the table data from DynamoDB
    try:
        response = tables_table.get_item(
            Key={'id': int(table_id)}  # Adjust this based on your key schema
        )
        
        # Check if the item was found
        if 'Item' not in response:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Table not found.'})
            }
        
        table_data = response['Item']
        
        # Prepare the response
        return {
            'statusCode': 200,
            'body': json.dumps(serialize_item(table_data))
        }
    
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error.'})
        }

# def get_table(event, table_id,tables_table):
#     response = tables_table.get_item(Key={'id': table_id})

#     print("---5-get_table--start")

  
#     if 'Item' in response:
         
#          item = {
#              'id': response['Item']["id"],
#              'number': response['Item']['number'],
#              'isVip': response['Item']['isVip'],
#              'minOrder': response['Item']['minOrder']
#              }
#          print("---5-get_table")
#          return {'statusCode': 200, 'body': json.dumps(item)}
#     else:
#         return {'statusCode': 400, 'body': json.dumps('Table not found')}


from boto3.dynamodb.conditions import Key
def create_reservation(event,reservations_table,tables_table):
    body = json.loads(event['body'])
    reservation_id = str(uuid.uuid4())
    
    print("---start 6-create_reservation-")


    response = reservations_table.scan(Limit=1)

     # Check if any items were found
    if 'Items' in response and response['Items']:
        print("---check tables---")
        print(body['tableNumber'])
        # table_exists = tables_table.query(
        # KeyConditionExpression=  Key('tableNumber').eq(int(body['tableNumber'])),
        # Limit=1)

        response = tables_table.scan(
            FilterExpression=Key('tableNumber').eq(int(body['tableNumber'])),
            Limit=1 
        )

        print("---done--")
    
        # if not table_exists['Items']:
        #     return {
        #         'statusCode': 404,
        #         'body': json.dumps({'error': 'Table not found.'})
        #     } 
        
        if not 'Items' in response and response['Items']:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Table not found.'})
            }
        
   
    
    # Create a new reservation entry
    item = {
        'id': reservation_id,
        'reservationId': reservation_id,
        'tableNumber': body['tableNumber'],
        'clientName': body['clientName'],
        'phoneNumber': body['phoneNumber'],
        'date': body['date'],
        'slotTimeStart': body['slotTimeStart'],
        'slotTimeEnd': body['slotTimeEnd']
    }
    print(item)

    # # Check for overlapping reservations
    # from boto3.dynamodb.conditions import Key
    # Check for overlapping reservations
    # overlapping_reservations = reservations_table.query(
    #     KeyConditionExpression=Key('id').eq(int(body['tableNumber'])),
    #     FilterExpression=(
    #         Key('date').eq(body['date']) & 
    #         (Key('slotTimeStart').lt(body['slotTimeEnd'])) & 
    #         (Key('slotTimeEnd').gt(body['slotTimeStart']))
    #     )
    # )
    
    # if overlapping_reservations['Items']:
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps({'error': 'Time slot overlaps with an existing reservation.'})
    #     }
    
    reservations_table.put_item(Item=item)
    print("---6-create_reservation-end")
    return {'statusCode': 200, 'body': json.dumps({'reservationId': reservation_id})}

def get_reservations(event,reservations_table):
    # Fetch reservations from DynamoDB
    response = reservations_table.scan()
    print("---7-get_reservations")
    return {'statusCode': 200, 'body': json.dumps({'reservations': response['Items']},default=convert_decimal_to_float)}