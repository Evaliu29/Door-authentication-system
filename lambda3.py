import json
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    # TODO implement
    if len(event) > 0:
        # id_recieved = event['id']
        content_recieved = event
    OTP = content_recieved["OTP"]
    dynamodb1 = boto3.resource('dynamodb', )
    table1 = dynamodb1.Table('passcodes')

    response = table1.query(
        KeyConditionExpression=Key('passcode').eq(OTP)
    )
    faceId = ""
    if len(response["Items"]) > 0:
        faceId = response['Items'][0]['faceId']
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("Wrong OTP")
        }
    print(faceId)
    dynamodb2 = boto3.resource('dynamodb', )
    table2 = dynamodb2.Table('visitors')

    response2 = table2.query(
        KeyConditionExpression=Key('faceId').eq(faceId)
    )
    print(response2)
    name = response2['Items'][0]['name']
    return {
        'statusCode': 200,
        'body': json.dumps(name)
    }
