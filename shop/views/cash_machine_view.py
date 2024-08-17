import os
from collections import Counter
from typing import List, Dict, Any
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from django.utils.timezone import now
from shop.models import Item
from shop.utils.pdf_generator import PDFGenerator
from shop.utils.qr_generator import QRCodeGenerator
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class CashMachine:
    """
    Класс для обработки логики кассового аппарата.

    Attributes:
        items (List[Item]): Список товаров.
        item_counts (Counter): Счетчик количества товаров.
        current_time (str): Текущее время.
        total_price (Decimal): Общая стоимость товаров.
        safe_time (str): Безопасное время для использования в именах файлов.
    """
    def __init__(self, items: List[Item], item_counts: Counter, current_time: str):
        """
        Инициализация CashMachine.

        Args:
            items (List[Item]): Список товаров.
            item_counts (Counter): Счетчик количества товаров.
            current_time (str): Текущее время.
        """
        self.items = items
        self.item_counts = item_counts
        self.current_time = current_time
        self.total_price = sum(item.price * item_counts[item.id] for item in items)
        self.safe_time = current_time.replace(" ", "_").replace(".", "-").replace(":", "-")

    def generate_receipt(self) -> str:
        """
        Генерация чека.

        Returns:
            str: Имя файла с чеком.
        """
        context: Dict[str, Any] = {
            'items': [(item, self.item_counts[item.id], item.price * self.item_counts[item.id]) for item in self.items],
            'total_price': self.total_price,
            'current_time': self.current_time,
        }

        pdf_filename: str = f'receipt_{self.safe_time}.pdf'
        pdf_path: str = os.path.join(settings.MEDIA_ROOT, pdf_filename)
        pdf_generator = PDFGenerator('receipt_template.html')
        pdf_generator.generate(context, pdf_path)

        return pdf_filename

    def generate_qr_code(self, pdf_url: str) -> str:
        """
        Генерация QR-кода.

        Args:
            pdf_url (str): URL для PDF-файла.

        Returns:
            str: Имя файла с QR-кодом.
        """
        qr_filename: str = f'qr_{self.safe_time}.png'
        qr_path: str = os.path.join(settings.MEDIA_ROOT, qr_filename)
        qr_generator = QRCodeGenerator()
        qr_generator.generate(pdf_url, qr_path)

        return qr_filename


class CashMachineView(APIView):
    """
    Представление для обработки запросов к кассовому аппарату.
    """
    def post(self, request: Request) -> JsonResponse:
        """
        Обработка POST-запроса.

        Args:
            request (Request): Запрос.

        Returns:
            JsonResponse: Ответ с URL QR-кода или сообщением об ошибке.
        """
        try:
            item_ids: List[int] = request.data.get('items', [])
            item_counts: Counter = Counter(item_ids)
            items: List[Item] = get_list_or_404(Item, id__in=item_counts.keys())
            current_time: str = now().strftime("%d.%m.%Y %H:%M")

            cash_machine = CashMachine(items, item_counts, current_time)
            pdf_filename = cash_machine.generate_receipt()
            pdf_url: str = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, pdf_filename))
            qr_filename = cash_machine.generate_qr_code(pdf_url)

            logger.info(f"PDF и QR-код успешно созданы: {pdf_filename}, {qr_filename}")
            return JsonResponse({'qr_code': request.build_absolute_uri(os.path.join(settings.MEDIA_URL, qr_filename))})
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {e}")
            return JsonResponse({'error': 'Ошибка при обработке запроса'}, status=500)