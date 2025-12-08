from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)


def get_db_connection():
    """
    Connexion à la base MySQL.

    - En LOCAL : ça utilise 127.0.0.1
    - En DOCKER : tu pourras définir MYSQL_HOST=db dans docker-compose
    """
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),  # 🔥 127.0.0.1 par défaut
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DATABASE", "comparateur"),
    )
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            phone_name,
            brand,
            website,
            price,
            currency,
            product_url,
            image_url
        FROM phones
        ORDER BY phone_name, brand, website, price
    """)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Si aucune donnée, on renvoie une liste vide
    if not rows:
        return render_template("index.html", phones=[], sites=[])

    # Liste des sites (colonnes)
    sites = sorted({row["website"] for row in rows})

    # Regroupement par téléphone
    phones_map = {}  # (phone_name, brand) -> dict

    for row in rows:
        key = (row["phone_name"], row["brand"])

        if key not in phones_map:
            phones_map[key] = {
                "phone_name": row["phone_name"],
                "brand": row["brand"],
                "offers": {}  # website -> offre
            }

        phones_map[key]["offers"][row["website"]] = {
            "price": row["price"],
            "currency": row["currency"],
            "product_url": row.get("product_url"),
            "image_url": row.get("image_url"),
        }

    # Calcul meilleur prix par téléphone
    phones = []
    for phone in phones_map.values():
        offers = phone["offers"]
        prices = [o["price"] for o in offers.values()]
        if prices:
            min_price = min(prices)
            for offer in offers.values():
                offer["is_best"] = (offer["price"] == min_price)
        phones.append(phone)

    # Tri des téléphones (optionnel)
    phones.sort(key=lambda p: (p["brand"], p["phone_name"]))

    return render_template("index.html", phones=phones, sites=sites)


if __name__ == "__main__":
    # En Docker, il faut écouter sur 0.0.0.0 pour être joignable de l'extérieur
    app.run(host="0.0.0.0", port=5000, debug=True)
