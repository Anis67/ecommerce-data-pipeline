import os
from dotenv import load_dotenv
from google.cloud import storage, bigquery

# === FORÇAGE DU .env (solution la plus fiable sur Windows) ===
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
env_path = os.path.join(project_root, ".env")

print("Project root détecté :", project_root)
print("Chemin .env utilisé  :", env_path)

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
    print("✅ .env chargé avec succès")
else:
    print("❌ Fichier .env introuvable à :", env_path)

# Debug des variables
print("GCP_PROJECT_ID              :", os.getenv("GCP_PROJECT_ID"))
print("GCP_BUCKET_NAME             :", os.getenv("GCP_BUCKET_NAME"))
print("GOOGLE_APPLICATION_CREDENTIALS :", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# === Configuration des credentials ===
creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if creds_path:
    # Si le chemin est relatif, on le rend absolu
    if not os.path.isabs(creds_path):
        creds_path = os.path.join(project_root, creds_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
    print("Credentials path final   :", creds_path)
else:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS non trouvé dans .env")

# ====================== Tests ======================
def test_gcs():
    try:
        client = storage.Client(project=os.getenv("GCP_PROJECT_ID"))
        bucket = client.get_bucket(os.getenv("GCP_BUCKET_NAME"))
        print(f"✅ GCS OK — bucket: {bucket.name}")
    except Exception as e:
        print(f"❌ Erreur GCS : {type(e).__name__} - {e}")

def test_bq():
    try:
        client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
        datasets = list(client.list_datasets())
        print(f"✅ BigQuery OK — datasets: {[d.dataset_id for d in datasets]}")
    except Exception as e:
        print(f"❌ Erreur BigQuery : {type(e).__name__} - {e}")

if __name__ == "__main__":
    test_gcs()
    test_bq()