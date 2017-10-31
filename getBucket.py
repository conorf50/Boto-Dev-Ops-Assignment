
#!/usr/bin/python3

import boto3

imgName = "image.png"
bucketName = "hi-conor-test"

def uploadFiles():
    # Create an S3 client
    print("Uploading" + str(imgName) + "to bucket")
    s3 = boto3.client("s3")
    # Boto 3
    bucket = s3.Bucket(bucketName)
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucketName)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False




# Define a main() function.
def main():
    uploadFiles()
      

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
