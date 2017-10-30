#!/usr/bin/python3


#Script Name: run_newwebserver.py
#Description: A Python 3 script to launch an Amazon instance, create and upload files to an S3 bucket and generate
# a web page that displays an image
#Author: Conor Farrell

import boto3
import time
import sys
import subprocess
import botocore



def createInstance():
    try:
        global sshKeyName
        sshKeyName = "ec2-key"

        global imageID
        imageID = 'ami-8c1be5f6'

        print("Creating a new instance")
        ec2 = boto3.resource('ec2')
        instances = ec2.create_instances(
            ImageId=imageID,           # ID for an Amazon Linux AMI in North Virginia
            KeyName=sshKeyName,                # existing key name that I have access to
            MinCount=1,
            MaxCount=1,
            SecurityGroupIds=['sg-9e34a7ec'], # Security group ID for 'HTTP and SSH'
            UserData='''#!/bin/bash
                        yum -y update
                        yum -y install nginx
                        yum -y install python35
                        service nginx start
                        chkconfig nginx on''', #run this shell script on the server
            InstanceType='t2.micro')
        
        global instanceName                     #defines the name as a global variable so that it can be accessed elsewhere
        instanceName = input("Please enter a name tag for your instance: ")
        name_tag = {'Key': 'Name', 'Value': instanceName} # allow the user to specify a name tag for the instance
        
        instance = instances[0]               # first element in list of instance objects

        instance.create_tags(Tags=[name_tag])


        print("Waiting for instance to initalise.")
        makeBucket()                            #go off and create an S3 bucket while we wait for the instance to install software
        instance.wait_until_running() # wait until the instance announces that it is running
        instance.reload()     # ensures instance object has current live instance data

        global instanceID   #global id variable
        instanceID = instance.id
        print ("An instance with ID", str(instanceID), "has been created.")

        global instanceIPAddress    #global in case we need it later on
        instanceIPAddress = instance.public_ip_address
        print("Your new instance IP address is " + str(instanceIPAddress))

    except botocore.exceptions.EndpointConnectionError as e:
        print("Could not connect to AWS. Check your internet connection")
        #exit if an error is encountered
        sys.exit(0)
    
    except botocore.exceptions.ClientError as InstanceLimitExceeded:
        print("You've exceeded your instance limit. Terminate unused instances and try again.") # Thanks Amazon...
        #exit if an error is encountered
        sys.exit(0)    




def makeBucket():        # Create an S3 client
    print("Starting")
    s3 = boto3.client("s3")
    print("Making a new bucket")
    #defines the bucket name as a global variable
    #See this answer for more info: 
    #https://stackoverflow.com/questions/36835812/how-to-call-a-variable-from-one-function-inside-another-function
    global bucketName
    bucketName = input("Please enter a unique name for your bucket: ")
    print("Name = ", bucketName)
    try:
        s3.create_bucket(Bucket=bucketName, ACL='public-read')

            # Call S3 to list current buckets
        print("Printing buckets")
        response = s3.list_buckets()

         # Get a list of all bucket names from the response
        print("All of your buckets.....")
        buckets = [bucket['Name'] for bucket in response['Buckets']]

                # Print out the bucket list
        print(buckets)    

    except botocore.exceptions.EndpointConnectionError as e:
        print("Could not connect to S3. Check your internet connection")
        sys.exit()

    except botocore.exceptions.ClientError as e:
        print("An error occured when creating your bucket")
        sys.exit()    

        #See the following for info about the below exception: https://github.com/boto/boto3/issues/1195
    except s3.exceptions.BucketAlreadyExists as e:  # Why is this different to the actual exception called when the name is not unique?
        print("This bucket name already exists. Please choose a different name")
        #terminateInstance()
        sys.exit()    





def terminateInstance():
    # Create an S3 client
    print("Terminating instance")
    s3 = boto3.client("s3")

    try:
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(instanceID)
        response = instance.terminate()
        print(response)

    except botocore.exceptions.EndpointConnectionError as e:
        print("Could not connect to S3. Check your internet connection")
        #exit if an error is encountered
        sys.exit()


def connectToInstance():
    # appending the file extension to the filename
    extendedKeyName = sshKeyName+".pem"
    # the hardcoded command to
    command="sudo pwd"
    fileName = "check_webserver.py" # hard code this for now, can be changed later
    filePath = '.' # this is the home folder

    print("Connecting to instance using key: " + str(extendedKeyName))

    # test an SSH connection to the instance
    commands = ['ssh', '-t', '-o', 'StrictHostKeyChecking=no', '-i', extendedKeyName, 'ec2-user@' + str(instanceIPAddress), command]
    commandString = ' '.join(commands) # convert the list of commands to a string so the command works. The ' ' keeps the spaces between the arguments
    (status, output) = subprocess.getstatusoutput(commandString)
    print(output)

    # scp a file up to the server
    cpToInstance = ['scp','-i', extendedKeyName, fileName, 'ec2-user@' + str(instanceIPAddress+':'+filePath)]
    commandString2 = ' '.join(cpToInstance) # convert the list of commands to a string so the command works
    print(commandString2)
    (status, output) = subprocess.getstatusoutput(commandString2)
    print(output)
    print(status)

    # change the permissions of the file
    chmodFile = ['ssh', '-i',extendedKeyName, 'ec2-user@' + str(instanceIPAddress), 'sudo chmod a+x',fileName]
    chmodCommand = ' '.join(chmodFile) # convert the list of commands to a string so the command works
    print(chmodCommand)
    (status, output) = subprocess.getstatusoutput(chmodCommand)
    print(output)
    print(status)

    # execute the  file
    executeFile = ['ssh', '-i',extendedKeyName, 'ec2-user@' + str(instanceIPAddress + ' ./'+fileName)]
    executeCommand = ' '.join(executeFile) # convert the list of commands to a string so the command works
    print(executeCommand)
    (status, output) = subprocess.getstatusoutput(executeCommand)
    print(output)
    print(status)





def main():
    global logfileName
    logTime = time.strftime("%d/%m/%Y-%H:%M:%S")
    logfileName = logTime+'.txt'
    print("Using logfile: " + str(logfileName))
    print("Starting script")
    createInstance()
    for x in range(1,3):
        print("Waiting to connect via SSH:")
        time.sleep(30)

    connectToInstance()    
  
      
if __name__ == '__main__':
    main()



