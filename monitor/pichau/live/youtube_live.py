from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from unshortenit import UnshortenIt
from monitor.pichau.buy.buy_pichau import PichauAutomator


def _setup_driver():
    options = Options()
    options.headless = True
    return Edge(options=options)


def _extract_message_info(message):
    author = message.find_element(By.CSS_SELECTOR, "#author-name").text
    text = message.find_element(By.CSS_SELECTOR, "#message").text
    return author, text


class YouTubeLiveChatScraper:
    def __init__(self):
        self.driver = _setup_driver()
        self.all_messages = []
        self.last_message_id = ""
        self.last_link_processed = ""
        self.pichau_automator = PichauAutomator()
        self.unshortener = UnshortenIt()

    def _is_link(self, keyword, text):
        words = text.split()
        for word in words:
            if keyword in word:
                expanded_url = self.unshortener.unshorten(word)
                if expanded_url and ("placa-de-video" in expanded_url or "processador" in expanded_url):
                    return True, expanded_url
        return False, None

    def scrape_live_chat(self,keyword, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "yt-live-chat-text-message-renderer"))
            )

            while True:
                new_message = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "yt-live-chat-text-message-renderer:last-of-type"))
                )
                new_message_id = new_message.get_attribute("id")

                if new_message_id != self.last_message_id:
                    author, text = _extract_message_info(new_message)
                    message = f"[{author}]: {text}"

                    is_link, link = self._is_link(keyword, text)
                    if is_link and link != self.last_link_processed:
                        print(f"Link detected: {message}")
                        self.last_link_processed = link
                        self.pichau_automator.run_automation_pix(link)

                    self.all_messages.append(message)
                    print(message)

                    self.last_message_id = new_message_id

        except KeyboardInterrupt:
            self.driver.quit()

