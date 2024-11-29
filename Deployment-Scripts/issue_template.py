try: 
    import os
    import re
    import json
    import base64
    import sys
    from github import Github
    from pprint import pprint
    
    print("All imports ok ...")

except Exception as e:
    print("Error Imports : {} ".format(e))
    
try:

#     Title = os.environ['ENROLLMENT_TITLE']
#     Message = os.environ['ENROLLMENT_MESSAGE']
#     RepoURL = os.environ['REPO_URL']
#     RepoName = os.environ['REPO_NAME'] 
#     IssueNumber = os.environ['ENROLLMENT_NUMBER']
#     token = os.environ['REPO_DISPATCH_PAT']
#     OWNER = 'Sanofi-GitHub'
#     REPO = 'snowflake-platform'
#     WORKFLOW2_NAME = 'si_repo_dispatch'
    
#     print("Processing request...")
#     print("Issue Title : {} ".format(Title))
#     print("Issue Message : {} ".format(Message))
    
#     if Title.lower()!="Create Storage Integration".lower():
#         print("Issue Title '{}' doesn't match : {} ".format(Title, "Create Storage Integration"))
   
    # lines = Message.splitlines()
    # #lines_var = lines
    # i=0

    # while i < len(lines):
    #    print("Line number: ", {i}, " : ", lines[i])
    #    i=i+1

    # try:
    #     lines = Message.splitlines()
    #     INPUT_ACCOUNT = lines[2]
    #     INPUT_DATABASE = lines[6]
    #     INPUT_INTEGRATION = lines[10]
    #     INPUT_AWS_ROLE_ARN = lines[14]
    #     INPUT_ALLOWED_LOCATIONS = lines[18]
        
    #     print("Input PVariable : INPUT_ACCOUNT: ", INPUT_ACCOUNT)
    #     print("Input PVariable : INPUT_DATABASE: ", INPUT_DATABASE)
    #     print("Input PVariable : INPUT_INTEGRATION: ", INPUT_INTEGRATION)
    #     print("Input PVariable : INPUT_AWS_ROLE_ARN: ", INPUT_AWS_ROLE_ARN)
    #     print("Input PVariable : INPUT_ALLOWED_LOCATIONS: ", INPUT_ALLOWED_LOCATIONS)

    #     #print("-------------------------------")
    #     #print("Triggering os.system for test: ")

    #     #import os 
    #     #import subprocess

    #     #print("PWD :", os.getcwd())
    #     #print("Triggering workflow_trigger.py using cmd:")

    #     #cmd="python workflow_trigger.py" +" "+ token +" "+ OWNER +" "+ REPO +" "+ WORKFLOW2_NAME +" "+ INPUT_ACCOUNT +" "+ INPUT_DATABASE +" "+ INPUT_INTEGRATION +" "+ INPUT_AWS_ROLE_ARN +" "+ INPUT_ALLOWED_LOCATIONS

    #     #print("cmd :", cmd)
        
    #     #subprocess.call(cmd, shell=True) 
        
    #     #execute("workflow_trigger.py", token, OWNER, REPO, WORKFLOW2_NAME, INPUT_ACCOUNT, INPUT_DATABASE, INPUT_INTEGRATION, INPUT_AWS_ROLE_ARN, INPUT_ALLOWED_LOCATIONS)
    #     #os.system('python workflow_trigger.py %s %s %s %s %s %s %s %s %s' % (token, OWNER, REPO, WORKFLOW2_NAME, INPUT_ACCOUNT, INPUT_DATABASE, INPUT_INTEGRATION, INPUT_AWS_ROLE_ARN, INPUT_ALLOWED_LOCATIONS))
    #     ##exec("python workflow_trigger.py", {'token':token, 'OWNER':OWNER, 'REPO':REPO, 'WORKFLOW2_NAME':WORKFLOW2_NAME, 'INPUT_ACCOUNT':INPUT_ACCOUNT, 'INPUT_DATABASE':INPUT_DATABASE, 'INPUT_INTEGRATION':INPUT_INTEGRATION, 'INPUT_AWS_ROLE_ARN':INPUT_AWS_ROLE_ARN, 'INPUT_ALLOWED_LOCATIONS':INPUT_ALLOWED_LOCATIONS})
        
    #     #print("-------------------------------")


    # except Exception as e:
    #        print("Error while initializing input variables : {} ".format(e))
    

    exit
except Exception as e:
    print("Script Error : {} ".format(e))

