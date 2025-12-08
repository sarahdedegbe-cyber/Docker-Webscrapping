import os
import mysql.connector
from itemadapter import ItemAdapter


class MySQLStorePipeline:
    def open_spider(self, spider):
        """
        Cette méthode établit la connexion MySQL au lancement du spider.
        Utilisation des variables d'environnement pour Docker ET local.
        """
        self.conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "root"),
            database=os.getenv("MYSQL_DATABASE", "comparateur"),
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """
        Fermeture propre et commit final.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        """
        Cette méthode reçoit un item Scrapy et l'insère dans MySQL.
        """
        adapter = ItemAdapter(item)

        # ---- Nettoyage du prix ----
        raw_price = adapter.get("price", "")
        if raw_price:
            price_str = (
                str(raw_price)
                .replace("€", "")
                .replace(",", ".")
                .replace("\u202f", "")  # espace fines non sécables
                .replace(" ", "")
            )

            try:
                price = float(price_str)
            except ValueError:
                price = None
        else:
            price = None

        sql = """
            INSERT INTO phones (phone_name, brand, website, price, currency, product_url, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            adapter.get("phone_name"),
            adapter.get("brand"),
            adapter.get("website"),
            price,
            adapter.get("currency", "EUR"),
            adapter.get("product_url"),
            adapter.get("image_url"),
        )

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except mysql.connector.Error as e:
            spider.logger.error(f"Erreur MySQL: {e}")

        return item
