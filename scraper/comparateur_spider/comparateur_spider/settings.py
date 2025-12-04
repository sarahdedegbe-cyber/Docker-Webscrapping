import os

BOT_NAME = "comparateur_spider"

SPIDER_MODULES = ["comparateur_spider.spiders"]
NEWSPIDER_MODULE = "comparateur_spider.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "comparateur_spider.pipelines.MySQLPipeline": 300,
}

# Configuration base de données (utilise les variables d'environnement Docker)
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")
DB_NAME = os.getenv("DB_NAME", "comparateur")
