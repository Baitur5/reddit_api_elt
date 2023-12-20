
import os
import boto3
from datetime import datetime
import sys
from load_from_s3_to_redshift import check_for_errors
from dotenv import load_dotenv

load_dotenv()
date = datetime.today().strftime('%d-%m-%Y')
FILE = f'result_{date}.csv000'

S3_BUCKET = os.getenv('S3_BUCKET')
IAM_ROLE = os.getenv("IAM_ROLE")
WORKGROUP = os.getenv('WORKGROUP')
DBT_TABLE = os.getenv('DBT_TABLE')

REDSHIFT_TO_CSV = (
    f"UNLOAD ('SELECT * FROM {DBT_TABLE}')"
    f"TO 's3://{S3_BUCKET}/{FILE}'"
    f"IAM_ROLE '{IAM_ROLE}'"
    "CSV PARALLEL OFF ALLOWOVERWRITE HEADER;"
)

def main():
    """
    Converts Redshift table to csv, uploads it to S3 and downloads it 
    """
    redshift_client = connect_to_redshift()
    statement_id = execute_statements(redshift_client)
    check_for_errors(redshift_client,statement_id)

    s3 = connect_to_s3()
    download_file(s3)
    
    

    
def connect_to_redshift():
    try:
        redshift_client = boto3.client('redshift-data',region_name="us-east-1")
        return redshift_client
    except Exception as e:
        print(f"Couldn't connect to redshift.Error: {e}")
        sys.exit(1)

def execute_statements(redshift_client):
    try:
        response = redshift_client.execute_statement(
            Database='dev',
            WorkgroupName=WORKGROUP,
            Sql = REDSHIFT_TO_CSV
        )
        return response['Id']

    except Exception as e:
        print(f"Couldn't execute statements.Error: {e}")
        sys.exit(1)

def connect_to_s3():
    try:
        s3 = boto3.resource('s3')
        return s3
    except Exception as e:
        print(f"Couldn't connect to S3.Error: {e}")
        sys.exit(1)


def download_file(s3):
    try:
        s3.Bucket(S3_BUCKET).download_file(FILE,f'./{FILE}')
    except Exception as e:
        print(f"Couldn't download file from S3. Error: {e}")
        sys.exit(1)
    
    

if __name__=="__main__":
    main()