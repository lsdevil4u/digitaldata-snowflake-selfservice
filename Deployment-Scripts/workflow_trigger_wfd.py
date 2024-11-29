import os
import requests
import sys

TOKEN= str(sys.argv[1])
OWNER= str(sys.argv[2])
REPO= str(sys.argv[3])
WORKFLOW_NAME= str(sys.argv[4])
INPUT_ACCOUNT= str(sys.argv[5])
INPUT_DATABASE= str(sys.argv[6])
INPUT_INTEGRATION= str(sys.argv[7])
INPUT_AWS_ROLE_ARN= str(sys.argv[8])
#INPUT_ALLOWED_LOCATIONS = ()
#INPUT_ALLOWED_LOCATIONS= sys.argv[9]
INPUT_ALLOWED_LOCATIONS= str(sys.argv[9])

print( "the toke value is")
def trigger_workflow(WORKFLOW_NAME,INPUT_ACCOUNT,INPUT_DATABASE,INPUT_INTEGRATION,INPUT_AWS_ROLE_ARN,INPUT_ALLOWED_LOCATIONS):

      headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {TOKEN}",
      }

      data = {
        "event_type": WORKFLOW_NAME,
        "client_payload": {
          'inputs_account': INPUT_ACCOUNT,
          'inputs_database': INPUT_DATABASE,
          'inputs_integration_name': INPUT_INTEGRATION,
          'inputs_AWS_ROLE_ARN': INPUT_AWS_ROLE_ARN,
          'inputs_ALLOWED_LOCATIONS': '{}'.format(INPUT_ALLOWED_LOCATIONS)    
        }
      }
      print("The client_payload ",data)

      responsevalue=requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",json=data,headers=headers)
      print("The respoinse message is ",responsevalue.content)

trigger_workflow(WORKFLOW_NAME,INPUT_ACCOUNT,INPUT_DATABASE,INPUT_INTEGRATION,INPUT_AWS_ROLE_ARN,INPUT_ALLOWED_LOCATIONS)
