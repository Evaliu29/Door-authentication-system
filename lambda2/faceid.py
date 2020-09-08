import boto3
## get the photo from S3
s3 = boto3.client("s3",region_name = 'us-east-1')
bucket = 'smartdoorphotobucket'
photo = 'taoxing.jpg'
photo_res = s3.get_object(Bucket=bucket, Key=photo)
photo_b = photo_res["Body"].read()

client = boto3.client('rekognition',region_name = 'us-east-1')

##get faceid from face_index by using photo.
collection_id = 'FaceRec'
response = client.index_faces(CollectionId=collection_id,
                              Image={'Bytes': photo_b, },
                              ExternalImageId=photo,
                              MaxFaces=1,
                              QualityFilter="AUTO",
                              DetectionAttributes=['ALL'])
get_faceid = response['FaceRecords'][0]['Face']['FaceId']

print(get_faceid)



