import qrcode
import logging

logger = logging.getLogger(__name__)

class QRCodeGenerator:
    """
    Класс для генерации QR-кодов.
    """
    def generate(self, data: str, output_path: str) -> None:
        """
        Генерация QR-кода.

        Args:
            data (str): Данные для кодирования в QR-код.
            output_path (str): Путь для сохранения QR-кода.
        """
        try:
            qr = qrcode.make(data)
            qr.save(output_path)
            logger.info(f"QR-код успешно создан: {output_path}")
        except Exception as e:
            logger.error(f"Ошибка при создании QR-кода: {e}")
            raise