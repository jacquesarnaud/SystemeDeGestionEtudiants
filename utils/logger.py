import logging


class LoggerUtils:
    def __init__(self):
        self.log = logging.basicConfig(
            filename="./utils/app.log",
            filemode="a",
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def log_info(self, message):
        logging.info(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_error(self, message):
        logging.error(message)
