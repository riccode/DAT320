from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
from utils.load_sloth import load_sloth
from utils.preprocess_sloth import preprocess_sloths
from utils.sloth_model import sloth_model
from utils.sloth_feature_importances import sloth_feature_importances
from utils.evaluate_sloths import evaluate_sloths
from utils.visualize_sloths import visualize_sloths
from datetime import datetime

#sloth pipeline run through an EDA pipeline to generate visualizations for a dashboard and evaluates default random forest and
#decision tree models

default_args= {
    'start_date': datetime(2021, 12, 1)
}

with DAG(
    "DAT320_project_pipeline",
    description='DAT320 Project Airflow ML Pipeline',
    schedule_interval='@daily',
    default_args=default_args, 
    catchup=False) as dag:

    # task: 1

    creating_classification_report_tracking_table = PostgresOperator(
        task_id="creating_classification_report_tracking_table",
        postgres_conn_id='postgres_default',
        sql='sql/create_sloth_classification_report.sql'
    )



    # task: 2.1
    visualize = PythonOperator(
        task_id='visualize',
        python_callable=visualize_sloths
    )

    # task: 2.2
    preprocessing = PythonOperator(
        task_id='preprocessing',
        python_callable=preprocess_sloths
    )

    # task: 3

    create_models = PythonOperator(
        task_id='create_models',
        python_callable=sloth_model
    )
        
    # task: 4

    feature_importances = PythonOperator(
        task_id='feature_importances',
        python_callable=sloth_feature_importances
    )

    # task: 5


    evaluate_models = PythonOperator(
        task_id='evaluate_models',
        python_callable=evaluate_sloths
    )

    creating_classification_report_tracking_table >> preprocessing >> visualize >> create_models >> feature_importances >> evaluate_models
