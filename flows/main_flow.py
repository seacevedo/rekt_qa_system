from prefect import flow
from bq_migrate import *
from fetch_hack_data import fetch_hack_data
from datetime import datetime


@flow(log_prints=True)
def run_pipeline(file_name: str, data_path: str) -> None:
    file_name_date = file_name + "_" + str(datetime.today().strftime("%Y-%m-%d")) + '.csv'
    fetch_hack_data(file_name_date, data_path)
    cloud_storage_upload(data_path, file_name_date)
    upload_data_bigquery(file_name_date)


if __name__ == '__main__':
    run_pipeline.serve(name="rekt-pipeline-deployment", cron="0 0 * * *")