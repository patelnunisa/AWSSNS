# Simple example with AWS SNS and Lambada analytics workload

The project aims to showcase how to trigger events and ingest data through aws services.

## Project overview
![awssns drawio (1)](https://user-images.githubusercontent.com/77594565/177031117-3d08b78e-4a06-4d80-ab9a-c2916d01c6cc.png)

## Config file
#### Database Configuration
- DB_USERNAME = "admin"
- DB_PASSWORD = "password"
- DB_NAME = "db"
- DB_ENDPOINT = "aws-sns-db.:***********:.us-east-1.rds.amazonaws.com"

#### Region
- AWS_REGION = 'us-east-1'

#### TOPICS
- ATTEMPTS_ARN = 'arn:aws:sns:us-east-1:***********:attempts'
- RECEIVED_ARN ='arn:aws:sns:us-east-1::***********::recieved'
- SUCCESSRATE_ARN ='arn:aws:sns:us-east-1::***********::successRate'

## Steps
- create Config.py file with all required credentials
- run init.py to create topics
- create lambda functions
- create database table
- run test_sns.py (using  python -m pytest) to test if all required topics and db connection are established
- run sns.py to enable data ingestion cycle shown in figure above

