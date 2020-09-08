import json
import cv2
import boto3
import base64
import time
from datetime import datetime
# from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    print(cv2.__version__)
    # TODO implement
    data_raw = event['Records'][0]['kinesis']['data']
    print(data_raw)
    data_str = base64.b64decode(data_raw).decode('ASCII')
    data = json.loads(data_str)
    
    # SNS and S3 client
    rekog = boto3.client('rekognition',
                        aws_access_key_id='aws_access_key_id',
                        aws_secret_access_key='aws_secret_access_key',
                        region_name='us-east-1')
    rekface = rekog.list_faces(CollectionId='FaceRec')
    print("rekog collection contains faces")
    print(rekface)
    s3 = boto3.client('s3',
                        aws_access_key_id='aws_access_key_id',
                        aws_secret_access_key='aws_secret_access_key',
                        region_name='us-east-1')
    sns = boto3.client('sns', aws_access_key_id='aws_access_key_id',
                       aws_secret_access_key='aws_secret_access_key',
                       region_name='us-east-1')
    
    # get fragment and save in s3
    KinesisVideo = data["InputInformation"]["KinesisVideo"]
    FragmentNumber = KinesisVideo["FragmentNumber"]
    kinesisvideo = boto3.client('kinesisvideo',
                          aws_access_key_id="aws_access_key_id",
                          aws_secret_access_key="aws_secret_access_key",
                          region_name='us-east-1')
    resp = kinesisvideo.get_data_endpoint(StreamName="ExampleStream",APIName='GET_MEDIA_FOR_FRAGMENT_LIST')
    data_url = resp['DataEndpoint']
    KinesisVideoArchive = boto3.client('kinesis-video-archived-media',
                            aws_access_key_id="aws_access_key_id",
                            aws_secret_access_key="aws_secret_access_key",
                            endpoint_url=data_url)
    response = KinesisVideoArchive.get_media_for_fragment_list(StreamName="ExampleStream",
            Fragments=[FragmentNumber])
    streamdata = response['Payload'].read()
    print("start saving")
    # save streamdata here
    f = open("/tmp/myAudio.mp4", 'wb')
    f.write(streamdata)
    f.close()
    
    FaceSearchResponse = data["FaceSearchResponse"]
    print(FaceSearchResponse)

    i = 0
    for faces in FaceSearchResponse:
        i += 1
        print("faces in FaceSearchResponse")
        
        # add photo lishengzhen.jpg here
        # response = s3.put_object(Body=streamdata, 
        #               Bucket = "smartdoorphotobucket", 
        #               Key = "demo.mp4")
        cap = cv2.VideoCapture("/tmp/myAudio.mp4")  
        ret, frame = cap.read()
        faceDetail = faces["DetectedFace"]
        widtho = 960
        heighto = 540
        width = faceDetail['BoundingBox'].get('Width')
        height = faceDetail['BoundingBox'].get('Height')
        left = faceDetail['BoundingBox'].get('Left')
        top = faceDetail['BoundingBox'].get('Top')
        w = int(width * widtho)
        h = int(height * heighto)
        x = int(left * widtho)
        y = int(top * heighto)
        image = frame[y:y+h, x:x+w]
        image_string = cv2.imencode('.jpg', image)[1].tostring()
        key = datetime.now().strftime("%Y%m%d%H%M%S")[2:] + 'p' + str(i) + '.jpg'
        response = s3.put_object(Body=image_string, 
                      Bucket = "smartdoorphotobucket", 
                      Key = key,
                      ACL='public-read',
                      ContentType= "images/jpeg")
        print("get s3 response")
        print(response)
        
        # get photo name and timestamp
        bucketname = 'smartdoorphotobucket'
        object = s3.get_object(Bucket=bucketname,Key=key)
        timestamp = object['LastModified'].strftime('%Y-%m-%dT%H:%M:%S')
        print(timestamp)
        
        if len(faces["MatchedFaces"]) != 0:
            print(faces["MatchedFaces"][0])
            faceid = faces["MatchedFaces"][0]["Face"]["FaceId"]
            #retrive info of the people from the db
            dynamodb = boto3.resource('dynamodb', aws_access_key_id='aws_access_key_id',
                                          aws_secret_access_key='aws_secret_access_key', region_name='us-east-2')
            table = dynamodb.Table('visitors')
            response = table.query(
                        KeyConditionExpression = Key('faceId').eq(faceid)
            )
            print("response")
            print(response)
            
            phoneNumber = response['Items'][0]["phoneNumber"]
            print(phoneNumber)
            
            # save new photo
            photos = response['Items'][0]["photos"]
            print(photos)
            new_photos = {"objectKey":key,"bucket":bucketname,"createdTimeStamp":timestamp}
            photos.append(new_photos)
            print(photos)
        
            table.update_item(
                Key={'faceId': "{UUID}" },
                UpdateExpression="set photos =:i",
                ExpressionAttributeValues={":i": photos},
                ReturnValues="UPDATED_NEW"
            )
            
                    
            # generate OTP and store in dynamodb
            dynamodb_code = boto3.resource('dynamodb', aws_access_key_id="aws_access_key_id",
                                      aws_secret_access_key="aws_secret_access_key",
                                      region_name='us-east-1')
            table_code = dynamodb_code.Table('passcodes')
            timestamp = int(time.time())
            otp = str(timestamp)
            print("otp is"+otp)
            timestamp_code = timestamp + 300
            db_info = {"faceId": faceid, "passcode": otp, "ttl": timestamp_code}
            dynamo_data = {key: value for key, value in db_info.items() if value}
            response2 = table_code.put_item(Item=dynamo_data)
            print(response2)
            print("finish create otp")
            # send message to realated people
            if response2['ResponseMetadata']['HTTPStatusCode'] != 200:
                print("Sorry, there is something wrong with system, please try again.")
            else:
                message = "Welcome, this is your otp: "+ otp
                phoneNumber = '+19293665135'
                sns.publish(
                    PhoneNumber=phoneNumber, Message=message
                )
                print("message "+message+" send successfully")
    
        else:
            # generate link of the website
            url = "http://visitorinfo.s3-website.us-east-2.amazonaws.com/?bucket="+bucketname + "&key="+key+"&timestamp="+timestamp
            phoneNumber = '+19293665135'
            message = "ALERT!\nAn unknown person is show up, please enter the website to check:\n"+ url
            sns.publish(
                PhoneNumber=phoneNumber, Message=message
            )
            print("message send successfully")
            
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
