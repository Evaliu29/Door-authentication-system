import boto3
import json

def add_faces_to_collection(bucket, photo, collection_id):
    s3 = boto3.client("s3")
    photo_res = s3.get_object(Bucket=bucket,Key=photo)
    photo_b = photo_res["Body"].read()

    client = boto3.client('rekognition')

    response = client.index_faces(CollectionId=collection_id,
                                  Image={'Bytes': photo_b,},
                                  ExternalImageId=photo,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])
    faceid = response['FaceRecords'][0]['Face']['FaceId']
    print(faceid)
    print('Results for ' + photo)
    # print(json.dumps(response,indent=2))
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])

def delete_faces_from_collection(collection_id, faces):
    client = boto3.client('rekognition')

    response = client.delete_faces(CollectionId=collection_id,
                                   FaceIds=faces)

    print(str(len(response['DeletedFaces'])) + ' faces deleted:')
    for faceId in response['DeletedFaces']:
        print(faceId)
    return len(response['DeletedFaces'])

def create_collection(collection_id):
    client = boto3.client('rekognition')

    # Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')


def list_faces_in_collection(collection_id):
    maxResults = 12
    faces_count = 0
    tokens = True

    client = boto3.client('rekognition')
    response = client.list_faces(CollectionId=collection_id,
                                 MaxResults=maxResults)

    print('Faces in collection ' + collection_id)

    while tokens:

        faces = response['Faces']

        for face in faces:
            print(face)
            faces_count += 1
        if 'NextToken' in response:
            nextToken = response['NextToken']
            response = client.list_faces(CollectionId=collection_id,
                                         NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens = False
    return faces_count


def main():
    collection_id = 'FaceRec'
    create_collection(collection_id)
    bucket = 'smartdoorphotobucket'
    photo1 = 'chenqian.jpg'
    photo2 = 'minyue.jpg'
    photo3 = 'taoxing.jpg'
    indexed_faces_count = add_faces_to_collection(bucket, photo1, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))
    indexed_faces_count = add_faces_to_collection(bucket, photo2, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))
    indexed_faces_count = add_faces_to_collection(bucket, photo3, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))

def adddengli():
    collection_id = 'FaceRec'
    bucket = 'smartdoorphotobucket'
    photo1 = 'lishengzhen.jpg'
    indexed_faces_count = add_faces_to_collection(bucket, photo1, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))

def addtaoxing():
    collection_id = 'FaceRec'
    bucket = 'smartdoorphotobucket'
    photo1 = 'taoxing.jpg'
    indexed_faces_count = add_faces_to_collection(bucket, photo1, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))

def delete():

    collection_id = 'FaceRec'
    faces = []
    faces.append("b61c660b-c358-4362-95af-24d93b0a85ef")

    faces_count = delete_faces_from_collection(collection_id, faces)
    print("deleted faces count: " + str(faces_count))

def list():
    collection_id = 'FaceRec'

    faces_count = list_faces_in_collection(collection_id)
    print("faces count: " + str(faces_count))
def deletecollection():
    collection_id = 'FaceRec'
    client = boto3.client('rekognition')
    response = client.delete_collection(CollectionId=collection_id)
    print(json.dumps(response,indent=2))

if __name__ == "__main__":
    main() # create collection and add faces
    # delete() # delete specific face
    # list() # list all face in collection
    # adddengli() # add dengli face
    # addtaoxing()
    # deletecollection()