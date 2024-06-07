import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CoinMarketCapScraper:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self, coin):
        self.coin = coin
        self.url = f"{self.BASE_URL}{coin}/"
        self.data = {}

    def scrape(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        try:
            driver.get(self.url)
            self.data["price"] = driver.find_element(By.CSS_SELECTOR, "div.priceValue").text
            self.data["price_change"] = driver.find_element(By.CSS_SELECTOR, "span.sc-15yy2pl-0").text
            self.data["market_cap"] = driver.find_element(By.XPATH, "//div[text()='Market Cap']/following-sibling::div").text
            self.data["market_cap_rank"] = driver.find_element(By.XPATH, "//div[text()='Market Cap Rank']/following-sibling::div").text
            self.data["volume"] = driver.find_element(By.XPATH, "//div[text()='Volume 24h']/following-sibling::div").text
            self.data["volume_rank"] = driver.find_element(By.XPATH, "//div[text()='Volume/Market Cap']/following-sibling::div").text
            self.data["volume_change"] = driver.find_element(By.XPATH, "//div[text()='Volume Change 24h']/following-sibling::div").text
            self.data["circulating_supply"] = driver.find_element(By.XPATH, "//div[text()='Circulating Supply']/following-sibling::div").text
            self.data["total_supply"] = driver.find_element(By.XPATH, "//div[text()='Total Supply']/following-sibling::div").text
            self.data["diluted_market_cap"] = driver.find_element(By.XPATH, "//div[text()='Fully Diluted Market Cap']/following-sibling::div").text
            self.data["contracts"] = [{"name": "solana", "address": driver.find_element(By.CSS_SELECTOR, "div.sc-16r8icm-0").text}]
            self.data["official_links"] = [{"name": "website", "link": driver.find_element(By.XPATH, "//a[text()='Website']").get_attribute("href")}]
            self.data["socials"] = [
                {"name": "twitter", "url": driver.find_element(By.XPATH, "//a[text()='Twitter']").get_attribute("href")},
                {"name": "telegram", "url": driver.find_element(By.XPATH, "//a[text()='Telegram']").get_attribute("href")}
            ]
        finally:
            driver.quit()

        return self.data
