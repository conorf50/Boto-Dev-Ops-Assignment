
#!/usr/bin/python3

import boto3
import botocore
import sys
import getopt
import time

def makeBucket():
    s3 = boto3.client("s3") # Create an S3 client
    print("Starting")
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


def uploadToBucket():       
    s3 = boto3.client("s3")
    global filename
    filename = 'laptop.jpg'
    print("Uploading file " + filename)

    s3.upload_file(filename, bucketName, filename,
    ExtraArgs={'ACL': 'public-read'}) #set the file to be publically accessible
    print("File uploaded")




def anotherFunction():
    print("The name of the newly created bucket is " + bucketName)
    #https//:s3.amazonaws.com/<bucket name>/<filename>
    print("The URI is : https//:s3.amazonaws.com/" +bucketName+'/'+filename)

# Define a main() function.
def main():
    global logFileName
    logTime = time.strftime("%d/%m/%Y-%H:%M:%S")
    logFileName = logTime+'.txt'
    makeBucket()
    uploadToBucket()
    anotherFunction()
# This is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
   main()
