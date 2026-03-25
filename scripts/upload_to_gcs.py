import os
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def upload_file_to_gcs(local_path: Path, bucket_name: str, gcs_path: str) -> None:
    client = storage.Client(project=os.getenv("GCP_PROJECT_ID"))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    blob.upload_from_filename(str(local_path))
    size_kb = local_path.stat().st_size / 1024

    logger.info(f"✅ Upload OK | {local_path.name} ({size_kb:.1f} KB) → gs://{bucket_name}/{gcs_path}")


def upload_daily_orders(date_str: str = None) -> None:
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    local_path = Path(f"data/raw/orders/date={date_str}/orders.jsonl")

    if not local_path.exists():
        logger.error(f"❌ Fichier introuvable : {local_path}")
        raise FileNotFoundError(f"Fichier manquant : {local_path}")

    bucket_name = os.getenv("GCP_BUCKET_NAME")
    gcs_path = f"raw/orders/date={date_str}/orders.jsonl"

    logger.info(f"Upload vers gs://{bucket_name}/{gcs_path}")
    upload_file_to_gcs(local_path, bucket_name, gcs_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Upload commandes vers GCS")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    upload_daily_orders(args.date)
    