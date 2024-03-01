from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from monitor.pichau.core.analyze_pichau import AnalyzePichau
from monitor.pichau.live.youtube_live import YouTubeLiveChatScraper
from src.controller.base_main import BaseMain
from src.telegram.notifier import Notifier as TelegramNotifier


class PichauMonitorController(BaseMain):
    def __init__(self):
        super().__init__()
        if self._config:
            self.notifier = TelegramNotifier()
            self.minimum_discount = 0
            self.wishlist = []
            self.running_ecommerce = False
            self.running_live = False
        else:
            raise ValueError("Telegram configurations not found in the configuration file.")

    def split_categories(self):
        if self._config and 'categorias' in self._config:
            self.running_ecommerce = True
            self.wishlist = []

            with ProcessPoolExecutor() as executor:
                for category, url in self._config['categorias'].items():
                    executor.submit(self.monitor_category, category, url)
        else:
            print("Settings not loaded or categories not found. Unable to start price monitoring.")

    def start_monitoring(self):
        if not self.running_ecommerce:
            process = multiprocessing.Process(target=self.split_categories)
            process.start()

    def stop_monitoring(self):
        self.running_ecommerce = False

    def restart_monitoring(self):
        self.stop_monitoring()
        self.start_monitoring()

    def monitor_category(self, category, url):
        while self.running_ecommerce:
            category_monitor = AnalyzePichau(category, url, self.get_controller_links(), [], self.get_notify())
            category_monitor.run()


def main():
    monitor = PichauMonitorController()
    monitor.start_monitoring()
    print("Starting monitoring...")


if __name__ == "__main__":
    main()
