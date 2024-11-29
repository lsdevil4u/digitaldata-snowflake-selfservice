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

    Title = os.environ['ENROLLMENT_TITLE']
    Message = os.environ['ENROLLMENT_MESSAGE']
    
    print("\nProcessing Issue template ...")
    print("\nIssue Title : {} ".format(Title))
    print("\nIssue Message : {} ".format(Message))
      
  #     if Title.lower()!="Create Storage Integration".lower():
  #         print("Issue Title '{}' doesn't match : {} ".format(Title, "Create Storage Integration"))
    
    lines = Message.splitlines()
    lines_var = lines
    i=0

    # while i < len(lines):
    #     print("Line number: ", {i}, " : ", lines[i])
    #     i=i+1

    lines = [l.strip() for l in Message.splitlines()]
    ##lines = Message.splitlines()
    PROJECT = lines[2].upper().strip()
    PROVIDER_ACCOUNT = lines[6].upper().strip().replace(".SNOWFLAKECOMPUTING.COM", "").replace("SANOFI-", "")
    PROVIDER_DB = lines[10].strip()
    PROVIDER_SCHEMA = lines[14].strip()
    PROVIDER_OBJECT = lines[18].strip()
    CONSUMER_ACCOUNT = lines[22].upper().strip().replace(".SNOWFLAKECOMPUTING.COM", "").replace("SANOFI-", "")
    CONSUMER_ROLE = lines[26].strip()
    ##INPUT_EMAIL = lines[30]


    # PROJECT = os.environ['INPUT_PROJECT'].upper().strip()
    # ##PROJECT = os.environ['INPUT_PROVIDER_DB'].upper().strip()
    # PROVIDER_ACCOUNT = os.environ['INPUT_PROVIDER_ACCOUNT'].upper().strip()
    # PROVIDER_DB = os.environ['INPUT_PROVIDER_DB'].upper().strip()
    # PROVIDER_SCHEMA = os.environ['INPUT_PROVIDER_SCHEMA'].upper().strip()
    # PROVIDER_OBJECT = os.environ['INPUT_PROVIDER_OBJECT'].upper().strip()
    # CONSUMER_ACCOUNT = os.environ['INPUT_CONSUMER_ACCOUNT'].upper().strip()
    # CONSUMER_ROLE = os.environ['INPUT_CONSUMER_ROLE'].upper().strip()
    # ##CONSUMER_RIGHT = os.environ['INPUT_CONSUMER_RIGHT'].upper().strip()
    CONSUMER_RIGHT = "SELECT"
    IssueNumber = os.environ['ENROLLMENT_NUMBER']
      
    print("\nInput from Issue template : PROJECT: ", PROJECT)
    print("\nInput from Issue template : PROVIDER_ACCOUNT: ", PROVIDER_ACCOUNT)
    print("\nInput from Issue template : PROVIDER_DB: ", PROVIDER_DB)
    print("\nInput from Issue template : PROVIDER_SCHEMA: ", PROVIDER_SCHEMA)
    print("\nInput from Issue template : PROVIDER_OBJECT: ", PROVIDER_OBJECT)
    print("\nInput from Issue template : CONSUMER_ACCOUNT: ", CONSUMER_ACCOUNT)
    print("\nInput from Issue template : CONSUMER_ROLE: ", CONSUMER_ROLE)
    print("\nInput from Issue template : CONSUMER_RIGHT: ", CONSUMER_RIGHT)
    print("\nInput from Issue template : IssueNumber: ", IssueNumber)

    #email = None
#     arn = None
#     account=INPUT_ACCOUNT
#     database=INPUT_DATABASE
#     integration=INPUT_INTEGRATION
#     location=INPUT_ALLOWED_LOCATIONS

    error_message = "Error: "

    provider_accountname = PROVIDER_ACCOUNT
    provideraccount = None
    if (provider_accountname.startswith("AMER_")) or (provider_accountname.startswith("EMEA_")):
        print("\nProvider Account Name meet requirements {}".format(provider_accountname))
        provideraccount = provider_accountname
    else: 
        print("\nProvider Account Name is not valid {}".format(provider_accountname))
        error_message = error_message + "Account Name is not valid. "  

    consumer_accountname = CONSUMER_ACCOUNT
    consumeraccount = None
    if (consumer_accountname.startswith("AMER_")) or (consumer_accountname.startswith("EMEA_")):
        print("\nConsumer Account Name meet requirements {}".format(consumer_accountname))
        consumeraccount = consumer_accountname
    else: 
        print("\nConsumer Account Name is not valid {}".format(consumer_accountname))
        error_message = error_message + "Account Name is not valid. "   
    
    
    rolename = CONSUMER_ROLE
    role = None
    if ('ACCOUNTADMIN' not in CONSUMER_ROLE) and CONSUMER_ROLE!= 'SECURITYADMIN' and CONSUMER_ROLE != 'SYSADMIN' and CONSUMER_ROLE != 'USERADMIN' and CONSUMER_ROLE != 'PUBLIC':
        print("\nRole meet requirements {}".format(rolename))
        role = rolename
    else: 
        print("\nThis Role is not allowed {}".format(rolename))
        error_message = error_message + "This Role is not allowed. "
    


    from github.MainClass import Github

    TOKEN = os.environ['REPO_DISPATCH_PAT']
    OWNER = 'Sanofi-GitHub'
    REPO = 'snowflake-platform'
    WORKFLOW_NAME = 'data_share_creation_repo_dispatch'
    # Title = os.environ['ENROLLMENT_TITLE']
    # Message = os.environ['ENROLLMENT_MESSAGE']
    # RepoURL = os.environ['REPO_URL']
    RepoName = os.environ['REPO_NAME'] 
    # IssueNumber = os.environ['ENROLLMENT_NUMBER']
    
    
    if error_message=="Error: " and provideraccount!=None and consumeraccount!=None:
        print("\nInput requirements are met !!")
    else:
        print("\nInput requirements does not met !!")
        print(error_message)
        g = Github(TOKEN)
        print("\nGithub : connected")
        repo = g.get_repo(RepoName)
        print("\nGithub Issue Update repo : {} ".format(repo))
        issue = repo.get_issue(number=int(IssueNumber))
        print("\nGithub Issue Update issue : {} ".format(issue))
        comment = issue.create_comment(error_message)
        print("\nGithub Issue Update comment : {} ".format(comment))
        status = issue.edit(state='closed')
        print("\nGithub Issue Update status : {} ".format(status))
        exit(error_message)

    
    headers = {
       "Accept": "application/vnd.github.v3+json",
       "Authorization": f"token {TOKEN}",
    }

    data = {
       "event_type": WORKFLOW_NAME,
       "client_payload": {
         'input_project': PROJECT,
         'input_provider_account': PROVIDER_ACCOUNT,
         'input_provider_db': PROVIDER_DB,
         'input_provider_schema': PROVIDER_SCHEMA,
         'input_provider_object': PROVIDER_OBJECT,
         'input_consumer_account': CONSUMER_ACCOUNT,
         'input_consumer_role': CONSUMER_ROLE,
         'input_consumer_right': CONSUMER_RIGHT,
         'issue_number': IssueNumber
        }
    }
    
    print("\nThe client_payload ",data)

    print("\nTriggering repository dispatch ...")

    responsevalue=requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",json=data,headers=headers)
    print("\nThe respoinse message is ",responsevalue.content)
    
except Exception as e:
       print("\nError while initializing input variables : {} ".format(e))

# try:
#     Title = os.environ['ENROLLMENT_TITLE']
#     Message = os.environ['ENROLLMENT_MESSAGE']
#     RepoURL = os.environ['REPO_URL']
#     RepoName = os.environ['REPO_NAME'] 
#     IssueNumber = os.environ['ENROLLMENT_NUMBER']
#     TOKEN = os.environ['REPO_DISPATCH_PAT']
    
#     print("\nUpdating issue details in Github for Issue number:", IssueNumber)

#     ##from github import Github
            
#     from github.MainClass import Github

#     g = Github(TOKEN)
#     print("\nGithub : connected")
#     repo = g.get_repo(RepoName)
#     print("\nGithub Issue Update repo : {} ".format(repo))
#     issue = repo.get_issue(number=int(IssueNumber))
#     print("\nGithub Issue Update issue : {} ".format(issue))
#     comment = issue.create_comment("Request processed successfully and provisioning is in progress, you will receive email notification with provisioning log, for any discrepancy please reach out Snowflake COE.\nNote: If AD group creation was selected, Email notification will be received after 2 hours, due to AD Sync jobs.\nExecution time may vary based on availability of Active, Sanofi Shared GitHub, runners.")
#     print("\nGithub Issue Update comment : {} ".format(comment))
#     status = issue.edit(state='closed')
#     print("\nGithub Issue Update status : {} ".format(status))
# except Exception as e:
#             print("\nGithub Issue Update error : {} ".format(e))
