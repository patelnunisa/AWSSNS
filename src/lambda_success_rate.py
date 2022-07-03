#
#   Authors:
#   Niki Patel, University of South Australia.
#

import json

def lambda_handler(event, context):
    # retrieve message from sns schema
    sucess_rate_json = json.loads(event['Records'][0]['Sns']['Message'])['responsePayload']
    print(sucess_rate_json)
    return sucess_rate_json
