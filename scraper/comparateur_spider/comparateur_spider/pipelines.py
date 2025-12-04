import mysql.connector

class MySQLPipeline:
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=spider.settings.get('DB_HOST'),
            user=spider.settings.get('DB_USER'),
            password=spider.settings.get('DB_PASSWORD'),
            database=spider.settings.get('DB_NAME'),
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        # site
        self.cursor.execute(
            "SELECT id FROM site WHERE name=%s",
            (item['site_name'],)
        )
        row = self.cursor.fetchone()
        if row:
            site_id = row[0]
        else:
            self.cursor.execute(
                "INSERT INTO site (name, url) VALUES (%s, %s)",
                (item['site_name'], item['product_url'])
            )
            self.conn.commit()
            site_id = self.cursor.lastrowid

        # product
        self.cursor.execute(
            "SELECT id FROM product WHERE name=%s",
            (item['product_name_normalized'],)
        )
        row = self.cursor.fetchone()
        if row:
            product_id = row[0]
        else:
            self.cursor.execute(
                "INSERT INTO product (name) VALUES (%s)",
                (item['product_name_normalized'],)
            )
            self.conn.commit()
            product_id = self.cursor.lastrowid

        # offer
        self.cursor.execute(
            """
            INSERT INTO offer (product_id, site_id, product_name_raw, price, product_url)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                product_id,
                site_id,
                item['product_name_raw'],
                item['price'],
                item['product_url'],
            )
        )
        self.conn.commit()

        return item
