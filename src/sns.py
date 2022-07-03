#
#   Authors:
#   Niki Patel, University of South Australia.
#

import json
import boto3
from config import ATTEMPTS_ARN,RECEIVED_ARN,AWS_REGION

sns_client = boto3.client('sns', region_name=AWS_REGION)

def publish_message(topic_arn, message, subject):
    """
    Publishes a message to a topic.
    """
    try:

        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject,
        )['MessageId']

    except ClientError:
        logger.exception(f'Could not publish message to the topic.')
        raise
    else:
        return response

if __name__ == '__main__':

    # publish message to attempts
    attempts_json =  json.load(open("event/attempts.json"))
    for json_dic in attempts_json:
        res = publish_message(ATTEMPTS_ARN, json.dumps(json_dic) , "attempts")
        print("attempts: ",res)

    # publish message to received
    received_json =  json.load(open("event/received.json"))
    for json_dic in received_json:
        response = publish_message(RECEIVED_ARN, json.dumps(json_dic) , "received")
        print("received: ",response)   
        
    