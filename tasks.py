
from celery import shared_task
from .utils import CoinMarketCapScraper

@shared_task
def scrape_coin_data(coin):
    scraper = CoinMarketCapScraper(coin)
    return scraper.scrape()
