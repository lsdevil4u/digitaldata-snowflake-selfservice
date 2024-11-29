try: 
    import os
    import requests
    import re
    import json
    import base64
    import sys
    ##import boto3
    import typing
    import json
    from github import Github
    from pprint import pprint
    
    print("\nAll imports ok ...")

except Exception as e:
    print("\nError Imports : {} ".format(e))
    
try:

    INPUT_ACCOUNT = os.environ['INPUT_ACCOUNT']
    INPUT_DATABASE = os.environ['INPUT_DATABASE']
    INPUT_ROLE = os.environ['INPUT_ROLE']
    INPUT_OWNER = os.environ['INPUT_OWNER']
    INPUT_WAREHOUSE = os.environ['INPUT_WAREHOUSE']
    INPUT_USER = os.environ['INPUT_USER']
    INPUT_IF_ADGROUP_CREATION_REQUIRED = os.environ['INPUT_IF_ADGROUP_CREATION_REQUIRED']
    INPUT_IF_WAREHOUSE_CREATION_REQUIRED = os.environ['INPUT_IF_WAREHOUSE_CREATION_REQUIRED']
    INPUT_IF_USER_CREATION_REQUIRED = os.environ['INPUT_IF_USER_CREATION_REQUIRED']
    INPUT_EMAIL = os.environ['INPUT_EMAIL']
    
    INPUT_ACCOUNT = INPUT_ACCOUNT.upper().strip()
    INPUT_DATABASE = INPUT_DATABASE.strip()
    INPUT_ROLE = INPUT_ROLE.upper().strip()
    ##INPUT_IF_ADGROUP_CREATION_REQUIRED = INPUT_IF_ADGROUP_CREATION_REQUIRED
    INPUT_OWNER = INPUT_OWNER.strip()
    ##INPUT_IF_WAREHOUSE_CREATION_REQUIRED = INPUT_IF_WAREHOUSE_CREATION_REQUIRED
    INPUT_WAREHOUSE = INPUT_WAREHOUSE.upper().strip()
    ##INPUT_IF_USER_CREATION_REQUIRED = INPUT_IF_USER_CREATION_REQUIRED
    INPUT_USER = INPUT_USER.upper().strip()
    INPUT_EMAIL = INPUT_EMAIL.lower().strip()
      
    print("\nInput from Issue template : INPUT_ACCOUNT: ", INPUT_ACCOUNT)
    print("\nInput from Issue template : INPUT_DATABASE: ", INPUT_DATABASE)
    print("\nInput from Issue template : INPUT_ROLE: ", INPUT_ROLE)
    print("\nInput from Issue template : INPUT_IF_ADGROUP_CREATION_REQUIRED: ", INPUT_IF_ADGROUP_CREATION_REQUIRED)
    print("\nInput from Issue template : INPUT_OWNER: ", INPUT_OWNER)
    print("\nInput from Issue template : INPUT_IF_WAREHOUSE_CREATION_REQUIRED: ", INPUT_IF_WAREHOUSE_CREATION_REQUIRED)
    print("\nInput from Issue template : INPUT_WAREHOUSE: ", INPUT_WAREHOUSE)
    print("\nInput from Issue template : INPUT_IF_USER_CREATION_REQUIRED: ", INPUT_IF_USER_CREATION_REQUIRED)
    print("\nInput from Issue template : INPUT_USER: ", INPUT_USER)
    print("\nInput from Issue template : INPUT_EMAIL: ", INPUT_EMAIL)


    email = None
#     arn = None
#     account=INPUT_ACCOUNT
#     database=INPUT_DATABASE
#     integration=INPUT_INTEGRATION
#     location=INPUT_ALLOWED_LOCATIONS

    error_message = "Error: "
    
    
    emailLine = INPUT_EMAIL
    emailcheck=re.match('^[A-Za-z0-9._%+-]+@sanofi.com$', emailLine)
    if emailcheck==None:
        print("\nemail address of Owner {} does not meet requirements".format(emailLine))
        error_message = error_message + "email address does not meet requirements."
        #exit
    else: 
        print("\nemail address check completed successfully for {}".format(emailLine))
        email = emailLine
    
    rolename = INPUT_ROLE
    role = None
    if ('ACCOUNTADMIN' not in INPUT_ROLE) and INPUT_ROLE!= 'SECURITYADMIN' and INPUT_ROLE != 'SYSADMIN' and INPUT_ROLE != 'USERADMIN':
        print("\nRole meet requirements {}".format(rolename))
        role = rolename
    else: 
        print("\nThis Role is not allowed {}".format(rolename))
        error_message = error_message + "This Role is not allowed"
    
#     arnLine = lines[14]
#     ##print(f"ARN role: {arnLine}")
#     arnCheck=re.match('^arn:aws:iam::\d{12}:role/.+', arnLine)

#     if arnCheck==None:
#         print("\nIAM Role ARN format {} does not meet requirements".format(arnLine))
#         error_message = error_message + "\nIAM Role ARN format does not meet requirements" 
#         exit
#     else:
#         print("\nIAM Role ARN check completed successfully for {}".format(arnLine))
#         arn = arnLine

    from github.MainClass import Github

    TOKEN = os.environ['REPO_DISPATCH_PAT']
    OWNER = 'Sanofi-GitHub'
    REPO = 'snowflake-platform'
    WORKFLOW_NAME = 'Custom_User_Role_Provisioning_JSON_TEST'
    IssueNumber = '12345789'
    
    
    if error_message=="Error: " and email!=None and role!=None and INPUT_ACCOUNT!=None and INPUT_DATABASE!=None and INPUT_ROLE!=None:
        print("\nInput requirements are met !!")
    else:
        print("\nInput requirements does not met !!")
        exit(error_message)

    
    headers = {
       "Accept": "application/vnd.github.v3+json",
       "Authorization": f"token {TOKEN}",
    }

    client_payload = {
         'inputs_account': INPUT_ACCOUNT,
         'inputs_database': INPUT_DATABASE,
         'input_role': INPUT_ROLE,
         'input_if_adgroup_creation_required': INPUT_IF_ADGROUP_CREATION_REQUIRED,
         'input_owner': INPUT_OWNER,
         'input_if_warehouse_creation_required': INPUT_IF_WAREHOUSE_CREATION_REQUIRED,
         'input_warehouse': INPUT_WAREHOUSE,
         'input_if_user_creation_required': INPUT_IF_USER_CREATION_REQUIRED,
         'input_user': INPUT_USER,
         'input_email': INPUT_EMAIL,
         'issuenumber': IssueNumber
        }

    data = {
       "event_type": WORKFLOW_NAME,
       "client_payload": {
         json.dumps(client_payload) 
        }
    }
    ##'payload_JSON': json.dumps(client_payload)

    print("\nThe client_payload ",data)

    print("\nTriggering repository dispatch ...")

    responsevalue=requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",json=data,headers=headers)
    print("\nThe respoinse message is ",responsevalue.content)
    
except Exception as e:
       print("\nError while initializing input variables : {} ".format(e))

