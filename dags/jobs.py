from datetime import datetime, timedelta
from uuid import uuid4
from airflow import DAG
import os
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
# from airflow.operators.python import ShortCircuitOperator

default_args = {
'owner'                 : 'airflow',
'description'           : 'KPMG use case pipeline',
'depend_on_past'        : False,
'start_date'            : datetime(2021, 5, 1),
'email_on_failure'      : False,
'email_on_retry'        : False,
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

with DAG('kpmg_use_case', default_args=default_args, schedule_interval="15 * * * *", catchup=False) as dag:
    pipeline_id = str(uuid4())

    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        

    scrape = DockerOperator(
        task_id='scrape_for_pdf',
        image='scraper:latest',
        container_name='scraper_task',
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER"),
            "APP_ID": os.getenv("APP_ID"),
            "API_ADMIN_KEY": os.getenv("API_ADMIN_KEY"),
            "DB_NAME": os.getenv("DB_NAME"),
            "PIPELINE_ID": pipeline_id
        }
    )

    # skip_tasks = ShortCircuitOperator(
    #     task_id="skip_tasks"
    # )
        
    extract_text = DockerOperator(
        task_id='extract_pdf_text',
        image='text_extractor:latest',
        container_name='text_extractor_task',
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER"),
            "APP_ID": os.getenv("APP_ID"),
            "API_ADMIN_KEY": os.getenv("API_ADMIN_KEY"),
            "DB_NAME": os.getenv("DB_NAME"),
            "PIPELINE_ID": pipeline_id
        }
    )

    classify_data = DockerOperator(
        task_id='classify_data',
        image='classification:latest',
        container_name='classification_task',
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "APP_ID": os.getenv("APP_ID"),
            "API_ADMIN_KEY": os.getenv("API_ADMIN_KEY"),
            "DB_NAME": os.getenv("DB_NAME"),
            "PIPELINE_ID": pipeline_id
        }
    )

    summarize_text = DockerOperator(
        task_id='summarize_text',
        image='summary:latest',
        container_name='summarize_text_task',
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "APP_ID": os.getenv("APP_ID"),
            "API_ADMIN_KEY": os.getenv("API_ADMIN_KEY"),
            "DB_NAME": os.getenv("DB_NAME"),
            "API_KEY_OPENAI": os.getenv("API_KEY_OPENAI"),
            "PIPELINE_ID": pipeline_id
        }
    )

    parent_comparison = DockerOperator(
        task_id='parent_comparison',
        image='compare_parent:latest',
        container_name='parent_comparison_task',
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "APP_ID": os.getenv("APP_ID"),
            "API_ADMIN_KEY": os.getenv("API_ADMIN_KEY"),
            "DB_NAME": os.getenv("DB_NAME"),
            "PIPELINE_ID": pipeline_id
        }
    )

    start_dag >> scrape 
    
    scrape >> extract_text

    extract_text >> classify_data

    classify_data >> summarize_text

    summarize_text >> parent_comparison

    parent_comparison >> end_dag