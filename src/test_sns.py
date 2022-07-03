#
#   Authors:
#   Niki Patel, University of South Australia.
#

"""
Unit tests for 
init.py (creat topic, list topic) and
sns.py (publish sns)
"""

import json
import os.path
import boto3
import pytest
import pymysql
from config import ATTEMPTS_ARN,RECEIVED_ARN,SUCCESSRATE_ARN,AWS_REGION,DB_USERNAME,DB_PASSWORD,DB_NAME,DB_ENDPOINT
import sns
sns_client = boto3.client('sns', region_name=AWS_REGION)

# test create topic - attempts
def test_create_topic():
    topic_attempts = sns_client.create_topic(Name="attempts")
    assert topic_attempts['TopicArn'] == ATTEMPTS_ARN

# test list all topics
def test_list_topics():
    topic_arns = [ATTEMPTS_ARN,RECEIVED_ARN,SUCCESSRATE_ARN]
    topic_list = []
    response = sns_client.list_topics()
    for item in response['Topics']:
        topic_list.append(item['TopicArn'])
    assert topic_list == topic_arns

# test publish message
def test_publish_message():
    response = sns_client.publish(
            TopicArn=ATTEMPTS_ARN,
            Message=json.dumps({
            "timestamp": "1656432000",
            "moduleid": "005f12966f",
            "tx_attempts": "3"
          }),
            Subject="test",
        )['ResponseMetadata']['HTTPStatusCode']
    assert response == 200

# check if db connected
def test_db_connect():
    # Connect to AWS RDS MySQL database
    connection = pymysql.connect(host=DB_ENDPOINT,user=DB_USERNAME,password=DB_PASSWORD,db=DB_NAME,connect_timeout=60)
    assert connection.open == True

# check if tables exist in db
def test_db_table_exist():
    tables =['attempts','received','success_rate']
    # Connect to AWS RDS MySQL database
    connection = pymysql.connect(host=DB_ENDPOINT,user=DB_USERNAME,password=DB_PASSWORD,db=DB_NAME,connect_timeout=60)
    cursor = connection.cursor()
    table_list = []
    cursor.execute('SHOW TABLES')
    for row in cursor:
        table_list.append(row[0])
    assert table_list == tables

# check if event files exist
def test_file_exist():
    assert (os.path.exists("event/received.json") and os.path.exists("event/attempts.json")) == True

