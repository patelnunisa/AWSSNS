#
#   Authors:
#   Niki Patel, University of South Australia.
#

import json
import pymysql
import time
from config import DB_USERNAME,DB_PASSWORD,DB_NAME,DB_ENDPOINT

try:
    # Connect to AWS RDS MySQL database
    connection = pymysql.connect(host=DB_ENDPOINT,user=DB_USERNAME,password=DB_PASSWORD,db=DB_NAME,connect_timeout=60)
except Exception as e:
    print("ERROR: ",e)
      
def get_last_event_time(data):
    try:
        # Connect to AWS RDS MySQL database
        cursor = connection.cursor()
        
        # Create a new record
        sql = "SELECT timestamp FROM `received` where moduleid = %s and id = (SELECT MAX(id) FROM `received` where moduleid = %s)"
        
        # Execute the query
        cursor.execute(sql, (data['moduleid'],data['moduleid']))
        for row in cursor:
            return row[0]
            
        return None    
    except Exception as e:
      print("ERROR Last Event: ",e)
      return None

def get_total_attempt(data,last_timestamp):
    try:
        cursor = connection.cursor()
        
        # Create a new record
        sql = ""
        if last_timestamp:
            sql = "SELECT max(`tx_attempts`) FROM `attempts` where `moduleid` = %s and (`timestamp` BETWEEN %s and %s)"
        else:
            sql = "SELECT max(`tx_attempts`) FROM `attempts` where `moduleid` = %s and `timestamp` >= %s"
            
        # Execute the query
        if not last_timestamp:
            cursor.execute(sql, (data['moduleid'],int(data['timestamp'])))
        elif int(data['timestamp']) > last_timestamp:
            cursor.execute(sql, (data['moduleid'],last_timestamp,int(data['timestamp'])))
        else:
            cursor.execute(sql, (data['moduleid'],int(data['timestamp']),last_timestamp))
            
        for row in cursor:
            return row[0]
            
        return None    
    except Exception as e:
      print("ERROR Total Attempt: ",e)
      return None
      
def insert_received_data(data):
    try:
        cursor = connection.cursor()
        
        # Create a new record
        sql = "INSERT INTO `received` (`moduleid`, `timestamp`, `received`) VALUES (%s, %s, %s)"
        
        # Execute the query
        cursor.execute(sql, (data['moduleid'],int(data['timestamp']),int(data['received'])))
        
        # Commit the change
        connection.commit()
      
    except Exception as e:
      print("ERROR Insert: ",e)
      
def insert_success_rate_data(data):
    try:
        cursor = connection.cursor()
        
        # Create a new record
        sql = "INSERT INTO `success_rate` (`moduleid`, `timestamp`, `success_rate`) VALUES (%s, %s, %s)"
        
        # Execute the query
        cursor.execute(sql, (data['moduleid'],int(data['timestamp']),float(data['success_rate'])))
        
        # Commit the change
        connection.commit()
      
    except Exception as e:
      print("ERROR Insert: ",e)
      
def lambda_handler(event, context):
    
    # retrieve message from sns schema
    received_json = json.loads(event['Records'][0]['Sns']['Message'])

    # get last time stamp to get the time range
    last_timestamp = get_last_event_time(received_json)
    
    #get total attempt from the last event
    total_attempt = get_total_attempt(received_json,last_timestamp)

    #calculate success rate based on received and attempted messages
    success_rate = (int(received_json['received']) / total_attempt) * 100
    success_rate_json = {
             "moduleid": received_json['moduleid'],
             "timestamp": int( time.time() ),
             "success_rate": round(success_rate,2)
    }
    
    # insert new received data
    insert_received_data(received_json)
    
    # insert new sucess rate data
    insert_success_rate_data(success_rate_json)
    
    return success_rate_json