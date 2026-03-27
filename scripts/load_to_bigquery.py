import os
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import bigquery, storage

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

SCHEMA = [
    bigquery.SchemaField("order_id",      "STRING",    mode="REQUIRED"),
    bigquery.SchemaField("customer_id",   "STRING",    mode="REQUIRED"),
    bigquery.SchemaField("product_name",  "STRING",    mode="NULLABLE"),
    bigquery.SchemaField("category",      "STRING",    mode="NULLABLE"),
    bigquery.SchemaField("price",         "FLOAT64",   mode="NULLABLE"),
    bigquery.SchemaField("quantity",      "INTEGER",   mode="NULLABLE"),
    bigquery.SchemaField("total_price",   "FLOAT64",   mode="NULLABLE"),
    bigquery.SchemaField("status",        "STRING",    mode="NULLABLE"),
    bigquery.SchemaField("country",       "STRING",    mode="NULLABLE"),
    bigquery.SchemaField("timestamp",     "TIMESTAMP", mode="NULLABLE"),
]


def create_table_if_not_exists(client: bigquery.Client, table_ref: str) -> None:
    try:
        client.get_table(table_ref)
        logger.info(f"Table {table_ref} existe déjà")
    except Exception:
        table = bigquery.Table(table_ref, schema=SCHEMA)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="timestamp"
        )
        client.create_table(table)
        logger.info(f"✅ Table créée : {table_ref}")


def load_jsonl_to_bigquery(date_str: str = None) -> None:
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    project_id  = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    dataset_id  = "ecommerce_raw"
    table_id    = "orders"
    table_ref   = f"{project_id}.{dataset_id}.{table_id}"
    gcs_uri     = f"gs://{bucket_name}/raw/orders/date={date_str}/orders.jsonl"

    client = bigquery.Client(project=project_id)

    create_table_if_not_exists(client, table_ref)

    job_config = bigquery.LoadJobConfig(
        schema=SCHEMA,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    logger.info(f"Chargement depuis {gcs_uri}...")
    load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    load_job.result()

    table  = client.get_table(table_ref)
    logger.info(f"✅ Chargement OK — {table.num_rows} lignes dans {table_ref}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chargement GCS → BigQuery")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    load_jsonl_to_bigquery(args.date)