FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Commande par défaut -> Dev A pourra changer
CMD ["scrapy", "crawl", "site1"]
