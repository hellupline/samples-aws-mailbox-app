import json

import boto3

from message_utils import Message, JSONEncoder


s3 = boto3.client("s3")


def lambda_handler(event, context) -> None:  # pylint: disable=unused-argument
    for record in event["Records"]:
        s3_event = record["s3"]
        bucket = s3_event["bucket"]["name"]
        key = s3_event["object"]["key"]
        r = s3.get_object(Bucket=bucket, Key=key)
        content = Message.from_bytes(r["Body"].read())
        print(json.dumps(content, cls=JSONEncoder))
