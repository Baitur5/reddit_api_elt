from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import datetime

@dag(
    dag_id="reddit_api_pipeline",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=True,
    dagrun_timeout=datetime.timedelta(minutes=15)
)
def Pipeline():

    extract_from_reddit = BashOperator(
        task_id="extract_from_reddit",
        bash_command="python3 /opt/airflow/extract_load/extract.py"
    )

    load_to_s3 = BashOperator(
        task_id="load_to_s3",
        bash_command="python3 /opt/airflow/extract_load/load_s3.py"
    )

    load_from_s3_to_redshift = BashOperator(
        task_id="load_from_s3_to_redshift",
        bash_command="python3 /opt/airflow/extract_load/load_from_s3_to_redshift.py"
    )
    
    extract_from_reddit>>load_to_s3>>load_from_s3_to_redshift
    
dg = Pipeline()

