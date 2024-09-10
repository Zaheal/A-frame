import logging
import logging.handlers
import time


class LoggerSetup:

    def __init__(self):
        self.logger = logging.getLogger('')
        self.setup_logging()

    def setup_logging(self):
        #  Формат логов
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        formatter = logging.Formatter(LOG_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        log_file = "logs/fastapi-elk.log"
        file = logging.handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", backupCount=5)
        file.setFormatter(formatter)

        self.logger.addHandler(console)
        self.logger.addHandler(file)
