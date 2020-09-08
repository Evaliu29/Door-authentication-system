import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
import time


def lambda_handler(event, context):
    # TODO implement

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb',  region_name='us-east-2')
    table = dynamodb.Table('visitors')
    timestamp = int(time.time())

    ## get the photo from S3
    s3 = boto3.client("s3", region_name='us-east-1')
    bucket = event['photos'][0]['bucket']
    photo = event['photos'][0]['objectKey']
    photo_res = s3.get_object(Bucket=bucket, Key=photo)
    photo_b = photo_res["Body"].read()

    client = boto3.client('rekognition',  region_name='us-east-1')

    ##get faceid from face_index by using photo.
    collection_id = 'FaceRec'
    response = client.index_faces(CollectionId=collection_id,
                                  Image={'Bytes': photo_b, },
                                  ExternalImageId=photo,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])
    get_faceid = response['FaceRecords'][0]['Face']['FaceId']

    # ##simulate the input and insert into the database
    faceid = get_faceid
    name = event["name"]
    phone = event["phonenumber"]
    photos = event["photos"]
    phonenum = "+1" + phone
    dynamo_info = {
        "faceId": faceid,
        "name": name,
        "phoneNumber": phonenum,
        "photos": photos
    }
    json.dumps(dynamo_info)

    dynamo_data = {key: value for key, value in dynamo_info.items() if value}
    response = table.put_item(Item=dynamo_data)

    # ##judge whether it is set in the db correctly
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        body_res = "Sorry, can not store the information, please try again."
    else:
        ##generate the otp
        dynamodb_code = boto3.resource('dynamodb',
                                       region_name='us-east-1')
        table_code = dynamodb_code.Table('passcodes')
        otp = str(timestamp)
        timestamp_code = timestamp + 300
        db_info = {"faceId": faceid, "passcode": otp, "ttl": timestamp_code}
        dynamo_data = {key: value for key, value in db_info.items() if value}
        response2 = table_code.put_item(Item=dynamo_data)
        if response2['ResponseMetadata']['HTTPStatusCode'] != 200:
            body_res = "Sorry, there is something wrong with system, please try again."
        else:
            body_res = "The information has been stored successfully! Message sent."
            # sns
            Message = "Welcome! This is your One-Time Passcode: " + otp
            # sns = boto3.client('sns',  region_name='us-east-1')
            # sns.publish(
            #     PhoneNumber=phonenum, Message=Message
            # )

    return {
        'statusCode': 200,
        # 'faceID': get_faceid,
        # 'body':
        'response': body_res,
        # 'event':event,
        # 'faceId':faceid,
        # 'name':name,
        # 'phone':phone,
        # "phonenum":phonenum,
        # 'photos':photos
    }



##retrive from the db
    # dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    # table = dynamodb.Table('visitors')
    # response = table.query(
    #             KeyConditionExpression = Key('faceId').eq("{UUID}")
    # )
    # print(response)
    # photos = response['Items'][0]["photos"]
    # print(photos)
    # new_photos = {}
    # new_photos = {"objectKey":"my-photo1.jpg","bucket":"my-photo-bucket","createdTimeStamp":timestamp}
    # photos.append(new_photos)
    # print(photos)

    # table.update_item(
    #     Key={'faceId': "{UUID}" },
    #     UpdateExpression="set photos =:i",
    #     ExpressionAttributeValues={":i": photos},
    #     ReturnValues="UPDATED_NEW"
    # )