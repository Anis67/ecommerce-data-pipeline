# 🛒 Ecommerce Data Pipeline

Pipeline de données e-commerce complet simulant un environnement data engineering en entreprise.

![CI](https://github.com/Anis67/ecommerce-data-pipeline/actions/workflows/ci.yml/badge.svg)

## Contexte

Tu es Data Engineer dans une startup e-commerce.
Objectif : construire une plateforme data complète qui ingère, transforme et rend exploitables les données de commandes clients.

## Architecture
```
[Python - fake_orders.py]
          ↓
[GCS - Raw Layer]
raw/orders/date=YYYY-MM-DD/orders.jsonl
          ↓
[Apache Spark - spark_transform.py]
          ↓
[GCS - Clean Layer]
clean/orders/*.parquet
          ↓
[dbt - models staging + marts]
          ↓
[BigQuery]
stg_orders / stg_customers
dim_customers / dim_products / fact_orders
          ↓
[Analytics SQL]

Orchestré par Apache Airflow (semaine 2)
```

## Stack technique

| Outil | Version | Rôle |
|-------|---------|------|
| Python | 3.10+ | Scripting & orchestration locale |
| Apache Spark | 3.5 | Traitement distribué (via Docker) |
| dbt Core | 1.7 | Modélisation data warehouse |
| Google Cloud Storage | - | Data lake (raw & clean) |
| BigQuery | - | Data warehouse analytique |
| Docker | - | Containerisation Spark |
| Apache Airflow | 2.8 | Orchestration (semaine 2) |
| GitHub Actions | - | CI/CD |

## Structure du projet
```
ecommerce-data-pipeline/
├── scripts/
│   ├── fake_orders.py          # Génération de données
│   ├── upload_to_gcs.py        # Upload vers GCS
│   ├── load_to_bigquery.py     # Chargement BigQuery
│   ├── spark_transform.py      # Transformation Spark
│   ├── run_pipeline.py         # Pipeline complet
│   └── test_gcp_connection.py  # Test connexion GCP
├── dbt/ecommerce/
│   └── models/
│       ├── staging/            # stg_orders, stg_customers
│       └── marts/              # dim_customers, dim_products, fact_orders
├── sql/                        # Requêtes analytiques BigQuery
├── dags/                       # DAGs Airflow (semaine 2)
├── infra/                      # Config infrastructure
├── tests/                      # Tests unitaires
├── docker-compose.yml          # Spark container
└── .env.example                # Template variables d'environnement
```

## Setup

### Prérequis
- Python 3.10+
- Docker Desktop
- Compte GCP avec BigQuery et Cloud Storage activés
- dbt Core (`pip install dbt-bigquery`)

### Installation
```bash
git clone https://github.com/Anis67/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
copy .env.example .env      # puis remplir les valeurs GCP
```

### Lancer le pipeline
```bash
# Pipeline complet (génération + upload GCS + Spark)
python scripts/run_pipeline.py

# Modèles dbt
cd dbt/ecommerce
dbt run
dbt test
```

## Modèle de données
```
fact_orders (1 ligne par commande)
├── order_id, customer_id, product_name
├── price, quantity, total_price
├── status, country, ordered_at
└── customer_segment (jointure dim_customers)

dim_customers
├── customer_id, country
├── total_orders, total_spent
└── customer_segment (Standard / Premium / VIP)

dim_products
├── product_name, category
├── total_revenue, avg_price
└── total_quantity_sold
```

## Requêtes SQL exemples
```sql
-- Chiffre d'affaires par pays
SELECT country, ROUND(SUM(total_price), 2) AS revenue
FROM `ecommerce-pipeline-dev.ecommerce_clean.fact_orders`
WHERE status = 'completed'
GROUP BY country
ORDER BY revenue DESC;

-- Répartition des segments clients
SELECT customer_segment, COUNT(*) AS nb_customers
FROM `ecommerce-pipeline-dev.ecommerce_clean.dim_customers`
GROUP BY customer_segment;
```

## Statut

- [x] Semaine 1 — Fondations & ingestion
  - [x] Setup projet & environnement
  - [x] GCP Cloud Storage & BigQuery
  - [x] Génération données & upload GCS
  - [x] Chargement BigQuery & SQL analytique
  - [x] Pipeline Spark (transformation & clean layer)
  - [x] dbt — modélisation data warehouse
- [ ] Semaine 2 — Orchestration & industrialisation
  - [ ] Airflow setup & DAGs
  - [ ] CI/CD GitHub Actions