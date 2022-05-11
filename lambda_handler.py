import os
import boto3

S3PREFIX = os.environ['S3PREFIX']

html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Data Coffee 🎧</title>
</head>
<body>
<img src="{s3prefix}{episode}.png" width="280px"><br>
<audio controls>
<source
src="{s3prefix}{episode}.mp3"
type="audio/mpeg">
</audio>
</body>
</html>
'''


def lambda_handler(event, context):
    s3 = boto3.session.Session(region_name="us-east-2").resource("s3")
    bucket = s3.Bucket('datacoffee-public')
    episodes = set()
    for obj in bucket.objects.filter(Prefix="episodes/"):
        try:
            episode, _ = obj.key.split('.')
            episodes.add(int(episode.split('episodes/')[1]))
        except Exception:
            pass
    latest = max(episodes)
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": html.format(episode=latest, s3prefix=S3PREFIX)
    }
