# ecommerce-data-pipeline

# 🛒 Ecommerce Data Pipeline

Pipeline de données e-commerce complet, construit en mode projet réel.

## Stack technique

| Outil | Rôle |
|-------|------|
| Python | Scripting & transformations |
| Apache Airflow | Orchestration |
| Apache Spark | Traitement distribué |
| dbt | Modélisation data warehouse |
| Google Cloud Storage | Data lake (raw & clean) |
| BigQuery | Data warehouse analytique |
| Docker | Containerisation |
| GitHub Actions | CI/CD |

## Architecture
```
[Python Script]
      ↓
[GCS - Raw Layer]  ← partitionné par date
      ↓
[Spark Job]
      ↓
[GCS - Clean Layer]  ← format Parquet
      ↓
[dbt models]
      ↓
[BigQuery]  ← fact_orders, dim_customers, dim_products
      ↓
[Analytics]

Orchestré par Apache Airflow
```

## Setup
```bash
git clone https://github.com/TON-USERNAME/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # puis remplir les valeurs
```

## Statut du projet

![CI](https://github.com/TON-USERNAME/ecommerce-data-pipeline/actions/workflows/ci.yml/badge.svg)

> Projet réalisé en 15 jours — simulation d'un environnement data engineering en entreprise.