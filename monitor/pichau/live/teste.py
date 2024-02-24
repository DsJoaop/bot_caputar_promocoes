from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from urllib.parse import urlparse
from unshortenit import UnshortenIt
from monitor.pichau.buy.buy_pichau import PichauAutomator

class YouTubeLiveChatScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._setup_driver()
        self.all_messages = []
        self.last_message_id = ""
        self.last_link_processed = ""
        self.pichau_automator = PichauAutomator()
        self.unshortener = UnshortenIt()

    def _setup_driver(self):
        options = Options()
        options.headless = True
        return Edge(options=options)

    def _extract_message_info(self, message):
        author = message.find_element(By.CSS_SELECTOR, "#author-name").text
        text = message.find_element(By.CSS_SELECTOR, "#message").text
        return author, text

    def _is_link(self, keyword, text):
        text = text
        keys = {'rtx', 'gtx', 'ryzen', 'rx', 'water', '550'}
        words = text.split()
        for word in words:
            if keyword in word:
                if any(key in word for key in keys):
                    return True, word
                else:
                    expanded_url = self.unshortener.unshorten(word)
                    if expanded_url and ("placa-de-video" in expanded_url or "processador" in expanded_url):
                        return True, expanded_url
        return False, None

    def scrape_live_chat(self, keyword):
        print("iniciado")

if __name__ == "__main__":
    youtube_url = "https://pruuu.me/3z1jz1i"
    link_url = "https"
    scraper = YouTubeLiveChatScraper(youtube_url)
    scraper._is_link(link_url, youtube_url)
