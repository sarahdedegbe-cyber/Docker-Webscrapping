from flask import Flask, render_template_string
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "pass"),
        database=os.getenv("DB_NAME", "comparateur"),
    )

TEMPLATE = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Comparateur de prix</title>
  <style>
    table { border-collapse: collapse; width: 80%; margin: auto; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background: #eee; }
    .best { font-weight: bold; color: green; }
    body { font-family: Arial, sans-serif; margin-top: 30px; }
  </style>
</head>
<body>
<h1 style="text-align:center;">Comparateur de prix</h1>
{% for product in products %}
  <h2 style="text-align:center;">{{ product.name }}</h2>
  <table>
    <tr>
      <th>Site</th>
      <th>Nom</th>
      <th>Prix</th>
      <th>Lien</th>
    </tr>
    {% for o in product.offers %}
    <tr>
      <td>{{ o.site_name }}</td>
      <td>{{ o.product_name_raw }}</td>
      <td class="{{ 'best' if o.is_best else '' }}">{{ o.price }} €</td>
      <td><a href="{{ o.product_url }}" target="_blank">Voir</a></td>
    </tr>
    {% endfor %}
  </table>
  <br>
{% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id as product_id,
            p.name as product_name,
            o.product_name_raw,
            o.price,
            o.product_url,
            s.name as site_name
        FROM product p
        JOIN offer o ON o.product_id = p.id
        JOIN site s ON s.id = o.site_id
        ORDER BY p.id, o.price ASC
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    products = []
    current_product_id = None
    current = None

    for r in rows:
        if r["product_id"] != current_product_id:
            if current:
                min_price = min(o["price"] for o in current["offers"])
                for o in current["offers"]:
                    o["is_best"] = (o["price"] == min_price)
                products.append(current)

            current_product_id = r["product_id"]
            current = {
                "id": r["product_id"],
                "name": r["product_name"],
                "offers": []
            }

        current["offers"].append({
            "site_name": r["site_name"],
            "product_name_raw": r["product_name_raw"],
            "price": float(r["price"]),
            "product_url": r["product_url"],
            "is_best": False
        })

    if current:
        min_price = min(o["price"] for o in current["offers"])
        for o in current["offers"]:
            o["is_best"] = (o["price"] == min_price)
        products.append(current)

    return render_template_string(TEMPLATE, products=products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
