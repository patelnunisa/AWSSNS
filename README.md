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

## Lambda function
### attempts
Create lambda function attemptLambda that triggers by attempt SNS
![image](https://user-images.githubusercontent.com/77594565/177065790-d292335f-aa65-45f1-9835-ee09581143e8.png)
### recieved
Create lambda function receivedtLambda that triggers by recieved SNS and the destination is success rate SNS
![image](https://user-images.githubusercontent.com/77594565/177065883-d154fb7f-9b25-401c-89af-b049ec8aa9d8.png)
### success rate
Create lambda function successRatetLambda that triggers by success rate SNS
![image](https://user-images.githubusercontent.com/77594565/177065919-d2995724-a23b-4514-a1c1-6224724cd93e.png)


## Steps
- create Config.py file with all required credentials
- run init.py to create topics
- create lambda functions
- create database table
- run test_sns.py (using  python -m pytest) to test if all required topics and db connection are established
- run sns.py to enable data ingestion cycle shown in figure above

