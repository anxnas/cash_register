import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.http import JsonResponse
from shop.models import Item
from shop.serializers import ItemSerializer
from shop.utils.pdf_generator import PDFGenerator
from shop.utils.qr_generator import QRCodeGenerator
from shop.views.cash_machine_view import CashMachineView
import json

class TestItemModel(unittest.TestCase):
    """
    Тесты для модели Item.
    """
    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.item = Item(title="Тестовый товар", price=100.00)

    def test_item_creation(self):
        """
        Тест создания товара.
        """
        self.assertEqual(self.item.title, "Тестовый товар")
        self.assertEqual(self.item.price, 100.00)

    def test_item_str(self):
        """
        Тест строкового представления товара.
        """
        self.assertEqual(str(self.item), "Тестовый товар")


class TestItemSerializer(unittest.TestCase):
    """
    Тесты для сериализатора ItemSerializer.
    """
    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.item = Item(title="Тестовый товар", price=100.00)
        self.serializer = ItemSerializer(instance=self.item)

    def test_serializer_fields(self):
        """
        Тест полей сериализатора.
        """
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'price']))
        self.assertEqual(data['title'], "Тестовый товар")
        self.assertEqual(data['price'], '100.00')


class TestPDFGenerator(unittest.TestCase):
    """
    Тесты для класса PDFGenerator.
    """
    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.pdf_generator = PDFGenerator('receipt_template.html')
        self.context = {'items': [], 'total_price': 0, 'current_time': '01.01.2023 12:00'}
        self.output_path = 'test_receipt.pdf'

    @patch('shop.utils.pdf_generator.render_to_string')
    @patch('shop.utils.pdf_generator.pdfkit.from_string')
    def test_generate_pdf(self, mock_from_string, mock_render_to_string):
        """
        Тест генерации PDF.
        """
        mock_render_to_string.return_value = '<html></html>'
        self.pdf_generator.generate(self.context, self.output_path)
        mock_render_to_string.assert_called_once_with('receipt_template.html', self.context)
        mock_from_string.assert_called_once_with('<html></html>', self.output_path)


class TestQRCodeGenerator(unittest.TestCase):
    """
    Тесты для класса QRCodeGenerator.
    """
    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.qr_generator = QRCodeGenerator()
        self.data = 'http://example.com'
        self.output_path = 'test_qr.png'

    @patch('shop.utils.qr_generator.qrcode.make')
    def test_generate_qr_code(self, mock_qrcode_make):
        """
        Тест генерации QR-кода.
        """
        mock_qr = MagicMock()
        mock_qrcode_make.return_value = mock_qr
        self.qr_generator.generate(self.data, self.output_path)
        mock_qrcode_make.assert_called_once_with(self.data)
        mock_qr.save.assert_called_once_with(self.output_path)


class TestCashMachineView(unittest.TestCase):
    """
    Тесты для представления CashMachineView.
    """
    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.factory = RequestFactory()
        self.view = CashMachineView.as_view()
        self.item = Item(id=1, title="Тестовый товар", price=100.00)

    @patch('shop.views.cash_machine_view.get_list_or_404')
    @patch('shop.views.cash_machine_view.CashMachine.generate_receipt')
    @patch('shop.views.cash_machine_view.CashMachine.generate_qr_code')
    def test_post(self, mock_generate_qr_code, mock_generate_receipt, mock_get_list_or_404):
        """
        Тест обработки POST-запроса.
        """
        mock_get_list_or_404.return_value = [self.item]
        mock_generate_receipt.return_value = 'receipt.pdf'
        mock_generate_qr_code.return_value = 'qr.png'

        request = self.factory.post('/cash_machine/', {'items': [1, 1, 2]})
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('qr_code', response_data)

if __name__ == '__main__':
    unittest.main()