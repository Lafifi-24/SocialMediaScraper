from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import sys
sys.path.insert(0, '/home/hamza/Documents/3WM_challenge/')
from processing import ProcessData

process = ProcessData()

files = {
    'x':'./memory/data/tweets_by_scraping.csv',
    'tiktok':'./memory/data/tiktok_by_scraping.csv',
    'output':'./memory/data/resultat.xlsx'
}


def process_data():
    process.process(files)
    process.save(files)

with DAG(
    dag_id="process_data",
    schedule=" * 1 * * * ",
    start_date=datetime(2023, 1, 1),
    tags=['process'],
) as dag:

    t1 = PythonOperator(
        task_id='simple_processing',
        python_callable=process_data,
    )

 