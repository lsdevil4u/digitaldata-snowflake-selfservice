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
    
    IssueNumber = os.environ['ENROLLMENT_NUMBER']
      
    print("\nInput from Issue template : PROJECT: ", PROJECT)
    print("\nInput from Issue template : PROVIDER_ACCOUNT: ", PROVIDER_ACCOUNT)
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
        print("\nAccount Name meet requirements {}".format(provider_accountname))
        provideraccount = provider_accountname
    else: 
        print("\nAccount Name is not valid {}".format(provider_accountname))
        error_message = error_message + "Account Name is not valid. "  
    
    from github.MainClass import Github

    TOKEN = os.environ['REPO_DISPATCH_PAT']
    OWNER = 'Sanofi-GitHub'
    REPO = 'snowflake-platform'
    WORKFLOW_NAME = 'data_share_deletion_repo_dispatch'
    # Title = os.environ['ENROLLMENT_TITLE']
    # Message = os.environ['ENROLLMENT_MESSAGE']
    # RepoURL = os.environ['REPO_URL']
    RepoName = os.environ['REPO_NAME'] 
    # IssueNumber = os.environ['ENROLLMENT_NUMBER']
    
    
    if error_message=="Error: " and provideraccount!=None:
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
