from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('UuidGenerator-handler')

import json
import uuid
import boto3
from datetime import datetime

# Initialize the S3 client
s3_client = boto3.client('s3')

class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """

        FLAG_TEST=True

        # Specify your S3 bucket name
        bucket_name = 'cmtr-1bb19304-uuid-storage'

        if FLAG_TEST:
            bucket_name=bucket_name+"-test"

        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        total_objects = sum(1 for _ in bucket.objects.all())
        print(total_objects)

        if int(total_objects) >= 11 :
            return 200
        else:
          
            # Generate 10 random UUIDs
            random_uuids = [str(uuid.uuid4()) for _ in range(10)]
            
            # Get the current execution start time
            execution_time = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
            
            
            # Create a file name using the execution time
            # file_name = f"{datetime.utcnow()}.json"

            if total_objects < 1 :
               file_name= "2024-01-01T00:00:00.000Z|2024-01-01T00:00:00.000000"
            else:
                dt = datetime.utcnow()
                # Format the datetime object to the desired ISO 8601 formats
                # iso_format_with_z = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"  # For '2024-01-01T00:00:00.000Z'
                # iso_format_with_microseconds = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")  # For '2024-01-01T00:00:00.000000'
                iso_format_with_z = dt.strftime("%Y-%m-%dT%H:%M") + ":00.000Z"  
                iso_format_with_microseconds = dt.strftime("%Y-%m-%dT%H:%M") + ":00.000000"  
                # Combine the two formats with a '|'
                file_name = f"{iso_format_with_z}|{iso_format_with_microseconds}"
                print(">>file_name : "+file_name)

            # print("1")
            # Prepare the content to be stored in the S3 bucket
            content = {
                "uuids": random_uuids,
                "execution_time": execution_time
            }
            
            # Convert content to JSON
            json_content = json.dumps(content)
            
            # print("2")
            # print(bucket_name)
            # print(file_name)
            # print(json_content)
            # print("3")
        
            try:
                # Upload the JSON file to S3
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=file_name,
                    Body=json_content,
                    ContentType='application/json'
                )
            except Exception as e:
                print(e)
            


            # print("4")

            # todo implement business logic
            return 200
    

HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
