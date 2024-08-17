from typing import Dict, Any
import pdfkit
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Класс для генерации PDF.

    Attributes:
        template_name (str): Имя шаблона для генерации PDF.
    """
    def __init__(self, template_name: str):
        """
        Инициализация PDFGenerator.

        Args:
            template_name (str): Имя шаблона для генерации PDF.
        """
        self.template_name = template_name

    def generate(self, context: Dict[str, Any], output_path: str) -> None:
        """
        Генерация PDF.

        Args:
            context (Dict[str, Any]): Контекст для шаблона.
            output_path (str): Путь для сохранения PDF.
        """
        try:
            html: str = render_to_string(self.template_name, context)
            pdfkit.from_string(html, output_path)
            logger.info(f"PDF успешно создан: {output_path}")
        except Exception as e:
            logger.error(f"Ошибка при создании PDF: {e}")
            raise