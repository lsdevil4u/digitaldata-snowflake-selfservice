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
    
    # lines = Message.splitlines()
    # lines_var = lines
    # i=0

    # while i < len(lines):
    #     print("Line number: ", {i}, " : ", lines[i])
    #     i=i+1

    lines = [l.strip() for l in Message.splitlines()]
    ##lines = Message.splitlines()
    INPUT_ACCOUNT = lines[2].upper().strip().replace(".SNOWFLAKECOMPUTING.COM", "").replace("SANOFI-", "")
    INPUT_DATABASE = lines[6].upper().strip()
    INPUT_INTEGRATION = lines[10].upper().strip()
    INPUT_AWS_ROLE_ARN = lines[14].strip()
    INPUT_ALLOWED_LOCATIONS = lines[18].replace(" ", "").strip()
    INPUT_EMAIL = lines[22].strip()
      
    print("\nInput from Issue template : INPUT_ACCOUNT: ", INPUT_ACCOUNT)
    print("\nInput from Issue template : INPUT_DATABASE: ", INPUT_DATABASE)
    print("\nInput from Issue template : INPUT_INTEGRATION: ", INPUT_INTEGRATION)
    print("\nInput from Issue template : INPUT_AWS_ROLE_ARN: ", INPUT_AWS_ROLE_ARN)
    print("\nInput from Issue template : INPUT_ALLOWED_LOCATIONS: ", INPUT_ALLOWED_LOCATIONS)
    print("\nInput from Issue template : INPUT_EMAIL: ", INPUT_EMAIL)

    email = None
    arn = None
    ##account=INPUT_ACCOUNT
    database=INPUT_DATABASE
    integration=INPUT_INTEGRATION
    location=INPUT_ALLOWED_LOCATIONS

    error_message = "Error: "

    accountname = INPUT_ACCOUNT
    account = None
    if (accountname.startswith("AMER_")) or (accountname.startswith("EMEA_")):
        print("\nAccount Name meet requirements {}".format(accountname))
        account = accountname
    else: 
        print("\nAccount Name is not valid {}".format(accountname))
        error_message = error_message + "Account Name is not valid. "  
    
    
    emailLine = INPUT_EMAIL
    emailcheck=re.match('^[A-Za-z0-9._%+-]+@sanofi.com$', emailLine)
    if emailcheck==None:
        print("\nEmail address {} does not meet requirements".format(emailLine))
        error_message = error_message + "email address does not meet requirements. "
        exit
    else: 
        print("\nEmail address check completed successfully for {}".format(emailLine))
        email = emailLine
    
    arnLine = INPUT_AWS_ROLE_ARN
    ##print(f"ARN role: {arnLine}")
    arnCheck=re.match(r'^arn:aws:iam::\d{12}:role/.+', arnLine)

    if arnCheck==None:
        print("\nIAM Role ARN format {} does not meet requirements".format(arnLine))
        error_message = error_message + "\nIAM Role ARN format does not meet requirements. " 
        exit
    else:
        print("\nIAM Role ARN check completed successfully for {}".format(arnLine))
        arn = arnLine

    from github.MainClass import Github

    TOKEN = os.environ['REPO_DISPATCH_PAT']
    OWNER = 'Sanofi-GitHub'
    REPO = 'snowflake-platform'
    WORKFLOW_NAME = 'si_repo_dispatch'
    Title = os.environ['ENROLLMENT_TITLE']
    Message = os.environ['ENROLLMENT_MESSAGE']
    RepoURL = os.environ['REPO_URL']
    RepoName = os.environ['REPO_NAME'] 
    IssueNumber = os.environ['ENROLLMENT_NUMBER']
    
    
    ##if error_message=="Error: " and arn!=None and email!=None and database!=None and integration!=None and location!=None:
    if error_message=="Error: " and arn!=None and email!=None and account!=None and database!=None and integration!=None and location!=None:
        print("\nStorage Itegration requirements are met !!")
    else:
        print("\nStorage Itegration requirements does not met !!")
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
         'inputs_account': INPUT_ACCOUNT,
         'inputs_database': INPUT_DATABASE,
         'inputs_integration_name': INPUT_INTEGRATION,
         'inputs_AWS_ROLE_ARN': INPUT_AWS_ROLE_ARN,
         'inputs_ALLOWED_LOCATIONS': '{}'.format(INPUT_ALLOWED_LOCATIONS),
         'inputs_EMAIL': INPUT_EMAIL,
         'issue_number': IssueNumber     
        }
    }
    
    print("\nThe client_payload ",data)

    print("\nTriggering repository dispatch ...")

    responsevalue=requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",json=data,headers=headers)
    print("\nThe response message is ",responsevalue.content)
    
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
#     comment = issue.create_comment("Your request for Storage Integration processed successfully and provisioning is in progress, you will receive email notification with provisioning log, for any discrepancy please reach out Snowflake COE.\nNote:Execution time may vary based on availability of Active, Sanofi Shared GitHub, runners.")
#     print("\nGithub Issue Update comment : {} ".format(comment))
#     status = issue.edit(state='closed')
#     print("\nGithub Issue Update status : {} ".format(status))
# except Exception as e:
#             print("\nGithub Issue Update error : {} ".format(e))
