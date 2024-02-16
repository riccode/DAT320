from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime
from utils.add_new_sloths import add_new_sloths

#this pipeline executes a single task. It calls "add_new_sloths" which adds a new procedurally generated sloth species to the 
#dataset

default_args= {
    'start_date': datetime(2021, 12, 1)
}

with DAG(
    "Update_sloths_pipeline",
    description='Update dashboard when new sloth data is available',
    schedule_interval='@daily',
    default_args=default_args, 
    catchup=False) as dag:
    

    with TaskGroup('new_sloths') as new_sloths:

        # task: 1
        preprocessing = PythonOperator(
            task_id='new_sloths',
            python_callable=add_new_sloths
        )

    new_sloths