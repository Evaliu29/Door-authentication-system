import boto3
import csv
import time

# Get the service resource.
dynamodb = boto3.resource('dynamodb', ,region_name='us-east-1')
table = dynamodb.Table('passcodes')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)




dynamo_info = {"faceId": "UU33", "passcode": "12334",
                 "ttl":int(time.time())}#str(datetime.now())
print(dynamo_info)
    # dynamo_data = {key: value for key, value in dynamo_info.items() if value}


response = table.put_item(Item=dynamo_info)

