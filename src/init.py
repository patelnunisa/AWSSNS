#
# Authors:
#   Niki Patel, University of South Australia.
#

import json
import logging
import boto3
from botocore.exceptions import ClientError
from config import ATTEMPTS_ARN,RECEIVED_ARN,SUCCESSRATE_ARN,AWS_REGION

sns_client = boto3.client('sns', region_name=AWS_REGION)


def create_topic(name):
    """
    Creates a SNS notification topic.
    """
    topic = None
    try:
        topic = sns_client.create_topic(Name=name)
    except ClientError:
        raise
    return topic

def list_topics():
    """
    Lists all SNS notification topics using paginator.
    """
    topics_list = []
    try:
        response = sns_client.list_topics()
        for item in response['Topics']:
            topics_list.append(item['TopicArn'])
    except ClientError:
        raise
    return topics_list


if __name__ == '__main__':

    # intialised all topics
    create_topic('attempts')
    create_topic('recieved')
    create_topic('successRate')

    # get list of ARN
    [ATTEMPTS_ARN,RECEIVED_ARN,SUCCESSRATE_ARN] = list_topics()