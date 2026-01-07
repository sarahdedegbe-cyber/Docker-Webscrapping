# Scrapy settings for comparateur_spider project

BOT_NAME = "comparateur_spider"

SPIDER_MODULES = ["comparateur_spider.spiders"]
NEWSPIDER_MODULE = "comparateur_spider.spiders"

# -------------------------------------------------
# 1) Respect des robots.txt
# -------------------------------------------------
# Pour le projet, on met False, sinon Scrapy ne scrapera pas Darty.
ROBOTSTXT_OBEY = False

# -------------------------------------------------
# 2) User-Agent (ça aide à éviter d’être bloqué trop vite)
# -------------------------------------------------
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}

# -------------------------------------------------
# 3) Concurrence de base
# -------------------------------------------------
CONCURRENT_REQUESTS = 8

DOWNLOAD_DELAY = 1.0  # petite pause entre les requêtes

# -------------------------------------------------
# 4) Cookies (pas forcément utiles ici)
# -------------------------------------------------
COOKIES_ENABLED = False

# -------------------------------------------------
# 5) Pipelines : on active la pipeline MySQL
# -------------------------------------------------
ITEM_PIPELINES = {
   # "comparateur_spider.pipelines.MySQLStorePipeline": 300,
}

# -------------------------------------------------
# 6) Encoding
# -------------------------------------------------
FEED_EXPORT_ENCODING = "utf-8"
