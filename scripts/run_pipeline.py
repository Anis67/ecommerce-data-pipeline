import argparse
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from fake_orders import generate_orders
from upload_to_gcs import upload_daily_orders

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def run_spark_in_docker(date_str: str) -> None:
    logger.info("Lancement du job Spark dans Docker...")
    result = subprocess.run(
        [
            "docker", "exec", "ecommerce-spark",
            "python3", "/opt/spark/work/scripts/spark_transform.py",
            "--date", date_str
        ],
        capture_output=False
    )
    if result.returncode != 0:
        raise RuntimeError("❌ Job Spark échoué")
    logger.info("✅ Job Spark terminé")


def run_pipeline(date_str: str) -> None:
    logger.info(f"=== Démarrage pipeline pour {date_str} ===")

    # Étape 1 — Génération locale
    output_path = Path(f"data/raw/orders/date={date_str}/orders.jsonl")
    generate_orders(1000, output_path)

    # Étape 2 — Upload GCS
    upload_daily_orders(date_str)

    # Étape 3 — Spark dans Docker
    run_spark_in_docker(date_str)

    logger.info(f"=== Pipeline terminé pour {date_str} ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()
    run_pipeline(args.date)