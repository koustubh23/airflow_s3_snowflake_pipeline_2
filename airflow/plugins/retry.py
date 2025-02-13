from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.dates import days_ago
from datetime import datetime
import requests
import os
import pandas as pd 
from io import StringIO


def get_data():
    url = 'https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD'

    response = requests.get(url)

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        data11= pd.read_csv(csv_data)
        print(data11.head())


        # Create the directory path if it doesn't exist
        data_dir = '/opt/airflow/data'
        print(data_dir)
        os.makedirs(data_dir, exist_ok=True)
        print(os.makedirs(data_dir, exist_ok=True))
        # Save the cleaned data to a new file
        data11.to_csv(f'{data_dir}/xrate2.csv', index=False)


def upload_data_to_s3():

    s3_hook = S3Hook(aws_conn_id='s3_conn')
    s3_hook.load_file(filename='/opt/airflow/data/xrate.csv',key='xrate3.csv',bucket_name ='airflows3dump')


def print_welcome():
    print('Welcome to Airflow!')


def print_date():
    print('Today is {}'.format(datetime.today().date()))


dag = DAG(
    'workflow_1',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False

)

print_welcome_task = PythonOperator (
    task_id='Task1',
    python_callable=print_welcome,
    dag=dag

)


print_date_task = PythonOperator(
    task_id='Task2',
    python_callable=print_date,
    dag=dag

)


upload_file = PythonOperator  (
    task_id='upload_data_to_s3',
    python_callable=upload_data_to_s3,
    op_kwargs = {
        'filename':'/opt/airflow/data/xrate.csv',
        'key':'xrate.csv',
        'bucket_name':'airflows3dump'},
    dag=dag

)


print_welcome_task >> print_date_task >>  upload_file