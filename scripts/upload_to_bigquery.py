import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas as pd

# Load .env file
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET    = os.getenv("GCP_DATASET")
TABLE      = os.getenv("GCP_TABLE")

# Verify they loaded correctly
print(f"Project: {PROJECT_ID}")
print(f"Dataset: {DATASET}")
print(f"Table:   {TABLE}")

client = bigquery.Client(project=PROJECT_ID)

# Create dataset
dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET}")
dataset_ref.location = "EU"
client.create_dataset(dataset_ref, exists_ok=True)
print(f"Dataset {DATASET} ready")

# Load CSV
df = pd.read_csv("data/raw_posts.csv")
df["post_date"] = pd.to_datetime(df["post_date"])

table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"
job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE",
    autodetect=True,
)
job = client.load_table_from_dataframe(
    df, table_id, job_config=job_config
)
job.result()

table = client.get_table(table_id)
print(f"Loaded {table.num_rows} rows into {table_id}")