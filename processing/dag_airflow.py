from airflow import DAG
from datetime import datetime


from processing import ProcessData

processer = ProcessData()

with DAG(
    dag_id="process_data",
    schedule_interval="@once",
    start_date=datetime(2021, 1, 1),
    tags=['process'],
) as dag:
    files = {
        'x':'./memory/data/tweets_by_scraping.csv',
        'tiktok':'./memory/data/tiktok_by_scraping.csv',
        'output':'./memory/data/resultat.xlsx'
    }
    processer.process(files)
    processer.save(files)