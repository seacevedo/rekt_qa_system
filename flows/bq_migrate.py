from prefect_gcp import GcpCredentials, GcsBucket
from prefect_gcp.bigquery import bigquery_load_cloud_storage
from prefect import task


@task(name="Uploading Hack Dataset to Google Cloud Storage", log_prints=True, retries=3)
def cloud_storage_upload(data_path: str, file_name: str) -> None:
    gcs_bucket =  GcsBucket.load("rekt-gcs")
    gcs_bucket.upload_from_path(from_path=data_path + '/' + file_name, to_path=file_name)


@task(name="Uploading Dataset from Bucket into BigQuery", log_prints=True, retries=3)
def upload_data_bigquery(file_name: str) -> None:
    gcp_credentials_block = GcpCredentials.load("gcp-creds")

    bigquery_load_cloud_storage(
        dataset="rekt_monitoring",
        table="documents",
        uri=f"gs://crypto_hack_docs/{file_name}",
        gcp_credentials=gcp_credentials_block,
        location='us',
    )


