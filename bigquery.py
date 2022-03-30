from google.oauth2 import service_account
from google.cloud import bigquery

from config import CREDENTIALS_PATH, PROJECT

def client_bigquery():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH)
    client = bigquery.Client(project=PROJECT, credentials=credentials)
    return client

def query_to_bigquery(query):
    client = client_bigquery()
    query_job = client.query(query)
    result = query_job.result()
    # dataframe = result.to_dataframe()
    return result
