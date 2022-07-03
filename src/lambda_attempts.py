#
#   Authors:
#   Niki Patel, University of South Australia.
#

import json
import pymysql
from config import DB_USERNAME,DB_PASSWORD,DB_NAME,DB_ENDPOINT

try:
    # Connect to AWS RDS MySQL database
    connection = pymysql.connect(host=DB_ENDPOINT,user=DB_USERNAME,password=DB_PASSWORD,db=DB_NAME,connect_timeout=60)
except Exception as e:
    print("ERROR: ",e)

def insert_attempts(data):
    try:
        # Connect to AWS RDS MySQL database
        cursor = connection.cursor()
        
        # Create a new record
        sql = "INSERT INTO `attempts` (`moduleid`, `timestamp`, `tx_attempts`) VALUES (%s, %s, %s)"
        
        # Execute the query
        cursor.execute(sql, (data['moduleid'],int(data['timestamp']),int(data['tx_attempts'])))
        
        # Commit the change
        connection.commit()
      
    except Exception as e:
      print("ERROR: ",e)
     
    finally:
        # close the database connection using close() method.
        connection.close()
        
def lambda_handler(event, context):
    json_subject = event['Records'][0]['Sns']['Subject']
    if json_subject != "test":
        json_message = json.loads(event['Records'][0]['Sns']['Message'])
        insert_attempts(json_message)
        return "data insered"
    else:
        return "test completed"