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
    INPUT_ROLE = lines[10].upper().strip()
    INPUT_IF_ADGROUP_CREATION_REQUIRED = lines[14]
    INPUT_OWNER = lines[18].lower().strip()
    INPUT_IF_WAREHOUSE_CREATION_REQUIRED = lines[22]
    INPUT_WAREHOUSE = lines[26].upper().strip()
    INPUT_IF_USER_CREATION_REQUIRED = lines[30]
    INPUT_USER = lines[34].upper().strip()
    INPUT_EMAIL = lines[38].lower().strip()
      
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


    
#     arn = None
#     account=INPUT_ACCOUNT
#     database=INPUT_DATABASE
#     integration=INPUT_INTEGRATION
#     location=INPUT_ALLOWED_LOCATIONS

    error_message = "Error: "

    accountname = INPUT_ACCOUNT
    account = None
    if (accountname.startswith("AMER_")) or (accountname.startswith("EMEA_")):
        print("\nAccount Name meet requirements {}".format(accountname))
        account = accountname
    else: 
        print("\nAccount Name is not valid {}".format(accountname))
        error_message = error_message + "Account Name is not valid. "  


    if INPUT_IF_ADGROUP_CREATION_REQUIRED=='Yes': 
        ownerLine = INPUT_OWNER
        owner = None
        owneremailcheck=re.match('^[A-Za-z0-9._%+-]+@sanofi.com$', ownerLine)
        if owneremailcheck==None:
            print("\nEmail address of Owner {} does not meet requirements".format(ownerLine))
            error_message = error_message + "email address of Owner does not meet requirements. "
            #exit
        else: 
            print("\nEmail address  of Owner - check completed successfully for {}".format(ownerLine))
            owner = ownerLine
    
    
    emailLine = INPUT_EMAIL
    email = None
    emailcheck=re.match('^[A-Za-z0-9._%+-]+@sanofi.com$', emailLine)
    if emailcheck==None:
        print("\nEmail address of requester {} does not meet requirements".format(emailLine))
        error_message = error_message + "email address of requester does not meet requirements. "
        #exit
    else: 
        print("\nEmail address of requester - check completed successfully for {}".format(emailLine))
        email = emailLine
    
    rolename = INPUT_ROLE
    role = None
    if (INPUT_DATABASE in INPUT_ROLE) and ('ACCOUNTADMIN' not in INPUT_ROLE) and ('SECURITYADMIN' not in INPUT_ROLE) and ('SECADMIN' not in INPUT_ROLE) and ('SYSADMIN' not in INPUT_ROLE) and INPUT_ROLE != 'USERADMIN':
        print("\nRole meet requirements {}".format(rolename))
        role = rolename
    else: 
        print("\nGiven role name is not allowed {}".format(rolename))
        error_message = error_message + "Given role name is not allowed. Role name must have DB Name in it."

    username = INPUT_USER
    user = None
    if (INPUT_DATABASE not in INPUT_USER) and INPUT_IF_USER_CREATION_REQUIRED=='Yes':
        print("\nService user name is not as per naming convention. {}".format(username))
        error_message = error_message + "Service user name is not as per  naming convention."
    else: 
        print("\nService User Name meet requirements {}".format(username))
        user = username
    
    from github.MainClass import Github

    TOKEN = os.environ['REPO_DISPATCH_PAT']
    OWNER = 'Sanofi-GitHub'
    REPO = 'snowflake-platform'
    WORKFLOW_NAME = 'custom_usr_role_warehouse_repo_dispatch'
    Title = os.environ['ENROLLMENT_TITLE']
    Message = os.environ['ENROLLMENT_MESSAGE']
    RepoURL = os.environ['REPO_URL']
    RepoName = os.environ['REPO_NAME'] 
    IssueNumber = os.environ['ENROLLMENT_NUMBER']
    
    
    #if error_message=="Error: " and owner!=None and email!=None and role!=None and INPUT_ACCOUNT!=None and INPUT_DATABASE!=None and INPUT_ROLE!=None:
    if error_message=="Error: " and account!=None and email!=None and role!=None and INPUT_ACCOUNT!=None and INPUT_DATABASE!=None and INPUT_ROLE!=None:
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
    
    COMBINED_MAIL = INPUT_EMAIL+","+INPUT_OWNER
    print("\nCOMBINED_MAIL: ", COMBINED_MAIL)

    data = {
       "event_type": WORKFLOW_NAME,
       "client_payload": {
         'inputs_account': INPUT_ACCOUNT,
         'inputs_database': INPUT_DATABASE,
         'input_role': INPUT_ROLE,
         'input_if_adgroup_creation_required': INPUT_IF_ADGROUP_CREATION_REQUIRED,
         ##'input_owner': INPUT_OWNER,
         'input_if_warehouse_creation_required': INPUT_IF_WAREHOUSE_CREATION_REQUIRED,
         'input_warehouse': INPUT_WAREHOUSE,
         'input_if_user_creation_required': INPUT_IF_USER_CREATION_REQUIRED,
         'input_user': INPUT_USER,
         'input_email': COMBINED_MAIL,
         'issue_number': IssueNumber
        }
    }
    
    print("\nThe client_payload ",data)

    print("\nTriggering repository dispatch ...")

    responsevalue=requests.post(f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",json=data,headers=headers)
    print("\nThe respoinse message is ",responsevalue.content)
    
except Exception as e:
       print("\nError while initializing input variables : {} ".format(e))

try:
    Title = os.environ['ENROLLMENT_TITLE']
    Message = os.environ['ENROLLMENT_MESSAGE']
    RepoURL = os.environ['REPO_URL']
    RepoName = os.environ['REPO_NAME'] 
    IssueNumber = os.environ['ENROLLMENT_NUMBER']
    TOKEN = os.environ['REPO_DISPATCH_PAT']
    
    print("\nUpdating issue details in Github for Issue number:", IssueNumber)

    ##from github import Github
            
    from github.MainClass import Github

    g = Github(TOKEN)
    print("\nGithub : connected")
    repo = g.get_repo(RepoName)
    print("\nGithub Issue Update repo : {} ".format(repo))
    issue = repo.get_issue(number=int(IssueNumber))
    print("\nGithub Issue Update issue : {} ".format(issue))
    comment = issue.create_comment("Request processed successfully and provisioning is in progress, you will receive email notification with provisioning log, for any discrepancy please reach out Snowflake COE.\nNote: If AD group creation was selected, Email notification will be received after 2 hours, due to AD Sync jobs.\nExecution time may vary based on availability of Active, Sanofi Shared GitHub, runners.")
    print("\nGithub Issue Update comment : {} ".format(comment))
    ##status = issue.edit(state='closed')
    ##print("\nGithub Issue Update status : {} ".format(status))
except Exception as e:
            print("\nGithub Issue Update error : {} ".format(e))
