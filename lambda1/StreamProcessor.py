import boto3
import json

def delete_stream_processors():
    client = boto3.client('rekognition')
    print('delete stream processor')
    res = client.stop_stream_processor(
        Name='StreamProcessorFaceRec'
    )
    response = client.delete_stream_processor(
        Name='StreamProcessorFaceRec'
    )
    print(json.dumps(response, indent=2))

def list_stream_processors():
    client = boto3.client('rekognition')
    print('list stream processor')
    response = client.list_stream_processors(
        MaxResults=12
    )
    print(json.dumps(response,indent=2))


def create_stream_processor(collection_id,collection_name):
    client = boto3.client('rekognition')

    # Create a collection
    # print('create stream processor for:' + collection_id)
    response = client.create_stream_processor(
        Input={
            'KinesisVideoStream': {
                'Arn':'arn:aws:kinesisvideo:us-east-1:422751436886:stream/ExampleStream/1571680283126'
            }
        },
        Output={
            'KinesisDataStream': {
                'Arn':'arn:aws:kinesis:us-east-1:422751436886:stream/faceRekog'
            }
        },
        Name=collection_name,
        Settings={
            'FaceSearch': {
                'CollectionId': collection_id,
                'FaceMatchThreshold': 80
            }
        },
        RoleArn='arn:aws:iam::422751436886:role/rekog'
    )
    print(json.dumps(response,indent=2))

def start_stream_processor(name):
    client = boto3.client('rekognition')
    response = client.start_stream_processor(
        Name=name
    )
    print(json.dumps(response,indent=2))

def main():
    collection_id = 'FaceRec'
    collection_name = 'StreamProcessorFaceRec'
    # create_stream_processor(collection_id,collection_name)
    # start_stream_processor(collection_name)
    list_stream_processors()
    # delete_stream_processors()

if __name__ == "__main__":
    main()