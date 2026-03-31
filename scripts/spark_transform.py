import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField,
    StringType, FloatType, IntegerType, TimestampType
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ====================== SCHEMA ======================
SCHEMA = StructType([
    StructField("order_id",     StringType(),    False),
    StructField("customer_id",  StringType(),    False),
    StructField("product_name", StringType(),    True),
    StructField("category",     StringType(),    True),
    StructField("price",        FloatType(),     True),
    StructField("quantity",     IntegerType(),   True),
    StructField("total_price",  FloatType(),     True),
    StructField("status",       StringType(),    True),
    StructField("country",      StringType(),    True),
    StructField("timestamp",    TimestampType(), True),
])


def create_spark_session() -> SparkSession:
    spark = SparkSession.builder \
        .appName("EcommerceTransform") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    return spark


def read_orders(spark: SparkSession, input_file: Path):
    logger.info(f"Tentative de lecture : {input_file}")
    logger.info(f"Fichier existe ? {input_file.exists()}")
    logger.info(f"Taille du fichier : {input_file.stat().st_size / 1024:.1f} KB")

    # On passe le chemin en string brute (le plus simple et souvent le plus fiable sur Windows)
    path_str = str(input_file)

    try:
        df = spark.read.schema(SCHEMA).json(path_str)
        count = df.count()
        logger.info(f"✅ Lecture réussie → {count:,} lignes")
        df.printSchema()
        return df
    except Exception as e:
        logger.error(f"❌ Erreur Spark : {type(e).__name__} → {e}")
        raise


def clean_orders(df):
    logger.info("Nettoyage...")
    df = df.dropDuplicates(["order_id"]) \
           .dropna(subset=["order_id", "customer_id"]) \
           .filter(F.col("price") > 0) \
           .filter(F.col("quantity") > 0) \
           .filter(F.col("status").isin(["completed", "pending", "cancelled", "refunded"]))
    logger.info(f"Lignes après nettoyage : {df.count():,}")
    return df


def enrich_orders(df):
    logger.info("Enrichissement...")
    df = df.withColumn("total_price_calculated", F.round(F.col("price") * F.col("quantity"), 2)) \
           .withColumn("is_high_value", F.when(F.col("total_price") > 200, True).otherwise(False)) \
           .withColumn("order_date", F.to_date(F.col("timestamp"))) \
           .withColumn("order_hour", F.hour(F.col("timestamp"))) \
           .withColumn("processed_at", F.current_timestamp())
    return df


def compute_aggregations(df):
    logger.info("Agrégations par catégorie...")
    agg = (
        df.filter(F.col("status") == "completed")
        .groupBy("category")
        .agg(
            F.count("*").alias("nb_orders"),
            F.round(F.sum("total_price"), 2).alias("revenue"),
            F.round(F.avg("price"), 2).alias("avg_price")
        )
        .orderBy(F.desc("revenue"))
    )
    agg.show(truncate=False)
    return agg


def write_parquet(df, output_dir: str):
    logger.info(f"Écriture Parquet dans : {output_dir}")
    (
        df.write
        .mode("overwrite")
        .partitionBy("order_date", "country")
        .parquet(output_dir)
    )
    logger.info("✅ Écriture Parquet terminée")


def run(date_str: str = None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "raw" / "orders" / f"date={date_str}" / "orders.jsonl"
    output_dir = str(project_root / "data" / "clean" / "orders")

    logger.info(f"Projet root : {project_root}")
    logger.info(f"Date traitée : {date_str}")

    if not input_file.exists():
        logger.error(f"❌ Fichier introuvable : {input_file}")
        raise FileNotFoundError(str(input_file))

    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    try:
        df = read_orders(spark, input_file)
        df = clean_orders(df)
        df = enrich_orders(df)
        compute_aggregations(df)
        write_parquet(df, output_dir)

        logger.info("🎉 Pipeline terminé avec succès !")
    finally:
        spark.stop()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=None)
    args = parser.parse_args()
    run(args.date)