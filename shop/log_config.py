import logging
from logging.handlers import RotatingFileHandler

class LogConfig:
    """
    Класс для настройки логирования.

    Attributes:
        log_file_name (str): Имя файла для логов.
        max_bytes (int): Максимальный размер файла логов в байтах.
        backup_count (int): Количество резервных копий файлов логов.
        encoding (str): Кодировка файла логов.
    """
    def __init__(self, log_file_name: str, max_bytes: int = 100*1024*1024, backup_count: int = 5, encoding: str = 'utf-8'):
        """
        Инициализация LogConfig.

        Args:
            log_file_name (str): Имя файла для логов.
            max_bytes (int): Максимальный размер файла логов в байтах.
            backup_count (int): Количество резервных копий файлов логов.
            encoding (str): Кодировка файла логов.
        """
        self.log_file_name = log_file_name
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.encoding = encoding

    def setup_logging(self) -> None:
        """
        Настройка логирования.
        """
        logger = logging.getLogger()
        handler = RotatingFileHandler(self.log_file_name, maxBytes=self.max_bytes, backupCount=self.backup_count, encoding=self.encoding)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)