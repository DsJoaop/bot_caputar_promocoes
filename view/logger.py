import logging;

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def log_error(self, message):
        self.logger.error(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)