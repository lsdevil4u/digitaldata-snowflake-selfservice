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
      
  #     if Title.lower()!="DB Provisioning".lower():
  #         print("Issue Title '{}' doesn't match : {} ".format(Title, "DB Provisioning"))
    
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
    INPUT_OWNER = lines[10].lower().strip()
    INPUT_MYAPPSID = lines[14].upper().strip()
    ONEMESH_DATA_ASSET_NAME = lines[18].upper().strip().replace(" ", "_")
    
      
    print("\nInput from Issue template : INPUT_ACCOUNT: ", INPUT_ACCOUNT)
    print("\nInput from Issue template : INPUT_DATABASE: ", INPUT_DATABASE)
    print("\nInput from Issue template : INPUT_OWNER: ", INPUT_OWNER)
    print("\nInput from Issue template : INPUT_MYAPPSID: ", INPUT_MYAPPSID)
    print("\nInput from Issue template : ONEMESH_DATA_ASSET_NAME: ", ONEMESH_DATA_ASSET_NAME)
    
    
   
#     arn = None
#     account=INPUT_ACCOUNT
#     database=INPUT_DATABASE
#     integration=INPUT_INTEGRATION
#     location=INPUT_ALLOWED_LOCATIONS
    
    error_message = "Error: "

    dbname=INPUT_DATABASE
    dbnamecheck=re.match('^[A-Za-z_][A-Za-z0-9_]*$', dbname)
    db = None
    if dbnamecheck==None:
        print("\nDB Name {} does not meet requirements".format(dbname))
        error_message = error_message + "DB Name is not valid. "
    else: 
        print("\nDB Name check completed successfully for {}".format(dbname))
        db = dbname
    
    accountname = INPUT_ACCOUNT
    account = None
    if (accountname.startswith("AMER_")) or (accountname.startswith("EMEA_")):
        print("\nAccount Name meet requirements {}".format(accountname))
        account = accountname
    else: 
        print("\nAccount Name is not valid {}".format(accountname))
        error_message = error_message + "Account Name is not valid. "    

    myappsidLine = INPUT_MYAPPSID
    myappsid = None
    myappscheck=re.match('^APM[0-9][0-9][0-9][0-9][0-9][0-9][0-9]$', myappsidLine)
    matches = ["APM0000000", "APM0000001", "APM0000002"]
    if myappscheck==None:
        print("\nMyAppsID does not meet requirements".format(myappsidLine))
        error_message = error_message + "MyAppsID does not meet requirements. "
        #exit
    elif any(x in myappsidLine for x in matches):
        print("\nInvalid MyAppsID".format(myappsidLine))
        error_message = error_message + "Invalid MyAppsID."
    else: 
        print("\nMyAppsID check completed successfully for {}".format(myappsidLine))
        myappsid = myappsidLine
    
    
    emailLine = INPUT_OWNER
    email = None
    emailcheck=re.match('^[A-Za-z0-9._%+-]+@sanofi.com$', emailLine)
    if emailcheck==None:
        print("\nEmail address of Owner {} does not meet requirements".format(emailLine))
        error_message = error_message + "email address does not meet requirements. "
        #exit
    else: 
        print("\nEmail address check completed successfully for {}".format(emailLine))
        email = emailLine
    
    from github.MainClass import Github

    TOKEN = os.environ['REPO_DISPATCH_PAT']
    OWNER = 'Sanofi-GitHub'
    REPO = 'snowflake-platform'
    WORKFLOW_NAME = 'db_provisioning_repo_dispatch'
    Title = os.environ['ENROLLMENT_TITLE']
    Message = os.environ['ENROLLMENT_MESSAGE']
    RepoURL = os.environ['REPO_URL']
    RepoName = os.environ['REPO_NAME'] 
    IssueNumber = os.environ['ENROLLMENT_NUMBER']
    
    ##if error_message=="Error: " and myappsid!=None and email!=None and INPUT_ACCOUNT!=None and INPUT_DATABASE!=None and INPUT_OWNER!=None and INPUT_MYAPPSID!=None:
    if error_message=="Error: " and account!=None and db!=None and myappsid!=None and email!=None and INPUT_ACCOUNT!=None and INPUT_DATABASE!=None and INPUT_OWNER!=None and INPUT_MYAPPSID!=None:
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
         'inputs_account': INPUT_ACCOUNT,
         'inputs_database': INPUT_DATABASE,
         'input_owner': INPUT_OWNER,
         'input_myappsid': INPUT_MYAPPSID,
         'issue_number': IssueNumber,
         'onemesh_data_asset_name': ONEMESH_DATA_ASSET_NAME   
        }
    }
    
    print("\nThe client_payload ",data)

    print("\nTriggering repository dispatch ...")

    responsevalue=requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",json=data,headers=headers)
    print("\nThe respoinse message is ",responsevalue.content)
    
except Exception as e:
       print("\nError while initializing input variables : {} ".format(e))
       exit()

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
#     comment = issue.create_comment("Request processed successfully and provisioning is in progress, you will receive email notification with provisioning log, for any discrepancy please reach out Snowflake COE.\nNote: Email notification will be received after 2 hours, due to AD Sync jobs.\nExecution time may vary based on availability of Active, Sanofi Shared GitHub, runners.")
#     print("\nGithub Issue Update comment : {} ".format(comment))
#     status = issue.edit(state='closed')
#     print("\nGithub Issue Update status : {} ".format(status))
# except Exception as e:
#             print("\nGithub Issue Update error : {} ".format(e))