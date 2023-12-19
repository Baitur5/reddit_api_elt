import os
import boto3
from datetime import datetime
import sys

S3_BUCKET = os.getenv('S3_BUCKET')

def main():
    """
    Connect to S3 bucket and upload our file
    """
    s3 = connect_to_s3()
    upload_file(s3)
    

def connect_to_s3():
    try:
        s3 = boto3.resource('s3')
        return s3
    except Exception as e:
        print(f"Couldn't connect to S3.Error: {e}")
        sys.exit(1)


def upload_file(s3):
    date = datetime.today().strftime('%d-%m-%Y')
    try:
        with open('/tmp/data.csv','rb') as file:
            s3.Bucket(S3_BUCKET).put_object(Key=f'data_{date}.csv',Body=file)
    except Exception as e:
        print(f"Couldn't upload file to S3. Error: {e}")
        sys.exit(1)
    
    

if __name__=="__main__":
    main()