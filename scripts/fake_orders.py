import json
import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path
from faker import Faker
import random
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

fake = Faker("fr_FR")

PRODUCTS = [
    {"name": "Laptop Pro 15", "category": "Électronique", "price_range": (800, 2000)},
    {"name": "Souris sans fil", "category": "Électronique", "price_range": (20, 80)},
    {"name": "Clavier mécanique", "category": "Électronique", "price_range": (60, 200)},
    {"name": "Écran 27 pouces", "category": "Électronique", "price_range": (200, 600)},
    {"name": "T-shirt coton bio", "category": "Vêtements", "price_range": (15, 45)},
    {"name": "Jean slim", "category": "Vêtements", "price_range": (40, 120)},
    {"name": "Veste imperméable", "category": "Vêtements", "price_range": (80, 250)},
    {"name": "Roman bestseller", "category": "Livres", "price_range": (8, 25)},
    {"name": "Livre Python avancé", "category": "Livres", "price_range": (25, 55)},
    {"name": "Casque audio", "category": "Électronique", "price_range": (50, 350)},
    {"name": "Chaise de bureau", "category": "Mobilier", "price_range": (150, 800)},
    {"name": "Lampe de bureau", "category": "Mobilier", "price_range": (30, 120)},
]

STATUSES = ["completed", "pending", "cancelled", "refunded"]
STATUS_WEIGHTS = [70, 15, 10, 5]

COUNTRIES = ["France", "Belgique", "Suisse", "Canada", "Maroc", "Tunisie"]


def generate_order() -> dict:
    product = random.choice(PRODUCTS)
    price = round(random.uniform(*product["price_range"]), 2)
    quantity = random.randint(1, 5)

    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": str(uuid.uuid4()),
        "product_name": product["name"],
        "category": product["category"],
        "price": price,
        "quantity": quantity,
        "total_price": round(price * quantity, 2),
        "status": random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0],
        "country": random.choice(COUNTRIES),
        "timestamp": fake.date_time_between(
            start_date="-1d", end_date="now"
        ).replace(tzinfo=timezone.utc).isoformat(),
    }


def generate_orders(n: int, output_path: Path) -> None:
    logger.info(f"Génération de {n} commandes...")
    orders = [generate_order() for _ in range(n)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for order in orders:
            f.write(json.dumps(order, ensure_ascii=False) + "\n")

    logger.info(f"✅ {n} commandes générées → {output_path}")
    return orders


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur de commandes e-commerce")
    parser.add_argument("--n", type=int, default=1000, help="Nombre de commandes")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"),
                        help="Date de partition (YYYY-MM-DD)")
    args = parser.parse_args()

    date_str = args.date
    output_path = Path(f"data/raw/orders/date={date_str}/orders.jsonl")
    generate_orders(args.n, output_path)