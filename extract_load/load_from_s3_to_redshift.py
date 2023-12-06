from datetime import datetime
import os
import sys
from time import sleep
import boto3
from dotenv import load_dotenv
import pathlib

IAM_ROLE = os.getenv("IAM_ROLE")
S3_BUCKET = os.getenv('S3_BUCKET')
WORKGROUP = os.getenv('WORKGROUP')

date = datetime.today().strftime('%d-%m-%Y')
file_path = f"s3://{S3_BUCKET}/data_{date}.csv" # file path to our file

create_table_if_not_exists = (
        "CREATE TABLE IF NOT EXISTS manhwa_subreddit( "
        "url VARCHAR(MAX), "
        "author VARCHAR(MAX), "
        "link_flair_text VARCHAR(MAX), "
        "title VARCHAR(MAX), "
        "score INT, "
        "num_comments INT, "
        "upvote_ratio FLOAT, "
        "created_utc TIMESTAMP, "
        "id VARCHAR PRIMARY KEY); ")

create_temp_table = "CREATE TABLE IF NOT EXISTS staging_table (LIKE manhwa_subreddit);"

# Insert data from file into our staging_table
sql_copy_to_temp = f"COPY dev.public.staging_table FROM '{file_path}' IAM_ROLE '{IAM_ROLE}' FORMAT AS CSV DELIMITER ','  IGNOREHEADER 1 REGION AS \'us-east-1\';"

# Insert into main table if not exists else update 
merge_temp_main_tables = ("MERGE INTO manhwa_subreddit USING staging_table as  st ON manhwa_subreddit.id = st.id "
"WHEN MATCHED THEN UPDATE SET score = st.score,num_comments = st.num_comments,upvote_ratio=st.upvote_ratio "
"WHEN NOT MATCHED THEN INSERT VALUES (st.url,st.author,st.link_flair_text,st.title,st.score,st.num_comments,st.upvote_ratio,st.created_utc,st.id);")

truncate_temp_table = "TRUNCATE TABLE staging_table;"

def main():
    """
    Upload S3 CSV data to Redshift
    """

    redshift_client = connect_to_redshift()

    statement_id = execute_statements(redshift_client)

    check_for_errors(redshift_client,statement_id)    
    

    
def connect_to_redshift():
    try:
        redshift_client = boto3.client('redshift-data',region_name="us-east-1")
        return redshift_client
    except Exception as e:
        print(f"Couldn't connect to redshift.Error: {e}")
        sys.exit(1)

def execute_statements(redshift_client):
    try:
        response = redshift_client.batch_execute_statement(
            Database='dev',
            WorkgroupName=WORKGROUP,
            Sqls=[
                create_table_if_not_exists,
                create_temp_table,
                sql_copy_to_temp,
                merge_temp_main_tables,
                truncate_temp_table
            ],
        )
        return response['Id']

    except Exception as e:
        print(f"Couldn't execute statements.Error: {e}")
        sys.exit(1)

# TODO: improve error handling when execuning sql statements
def check_for_errors(redshift_client,statement_id):
    """ 
    If statement has status 'FAILED' throw an Exception
    """
    try: 
        while True:
            describe = redshift_client.describe_statement(Id=statement_id)
            status = describe['Status']
            status_arr = ['FINISHED', 'FAILED', 'ABORTED']
            if status in status_arr:
                if status=='FAILED':raise Exception(describe)
                break
            sleep(3)  
    except Exception as e:
        print(f"Couldn't execute statements.Error: {e}")
        sys.exit(1)


if __name__=="__main__":
    main()
