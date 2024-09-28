from google.oauth2 import service_account
import pandas_gbq
import pandas as pd


def get_credentials() -> service_account.Credentials:
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            '/home/seacevedo/app/.creds/gcreds.json',
        )
        return credentials
    except FileNotFoundError:
        cred_err = "Credential JSON File Not Found"
        print(cred_err)

def retrieve_documents() -> dict:
    creds = get_credentials()
    sql = """
    SELECT *
    FROM `rekt_monitoring.documents`
    """
    try:
        print("Retrieving Data from BigQuery Documents Table...")
        df_rekt = pandas_gbq.read_gbq(sql, project_id="rekt-chat-435301", credentials=creds)
        return df_rekt.to_dict(orient='records')
    except Exception as e:
        print(e)


def append_metrics(metrics_data: dict) -> None:
    creds = get_credentials()
    df_metrics = pd.DataFrame.from_dict(metrics_data, orient="index").T
    df_metrics["response_time"] = pd.to_numeric(df_metrics["response_time"], downcast='float')
    df_metrics["cosine_similarity"] = pd.to_numeric(df_metrics["cosine_similarity"], downcast='float')
    print(df_metrics)
    try:
        print("Appending Metrics to BigQuery Metrics Table...")
        pandas_gbq.to_gbq(df_metrics, "rekt_monitoring.metrics", project_id="rekt-chat-435301", credentials=creds, if_exists='append')
    except Exception as e:
        print(e)

    
