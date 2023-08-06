import os
import boto3
import html
import json

DYNAMO_TABLE = os.environ['TABLE']
S3PREFIX = os.environ['S3PREFIX']
with open('index.html', 'r') as file:
    INDEX = file.read()

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMO_TABLE)
    items = table.scan()
    published = []
    
    # querying database
    for i in items['Items']:
        if 'meta' in i.keys() and i['meta']['published']:
            published.append(i)
    
    # preparing playlist
    playlist = []
    for record in sorted(published, reverse=True, key=lambda x: int(x['episode'].split("-")[-1])):
        meta = record['meta']
        episode_number = record['episode']
        title = f'{episode_number}. {meta["title"]}'
        file = f'{S3PREFIX}{record["episode"]}.mp3'
        playlist.append({"title": title, "file": file, "howl": None})

    playlist_str = json.dumps(playlist)
    
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": INDEX.format(playlist=playlist_str)
    }
