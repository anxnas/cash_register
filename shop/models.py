from django.db import models

class Item(models.Model):
    """
    Модель для представления товара.

    Attributes:
        title (str): Наименование товара.
        price (Decimal): Стоимость товара.
    """
    title = models.CharField(max_length=255, verbose_name="Наименование")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        """
        Возвращает строковое представление товара.

        Returns:
            str: Наименование товара.
        """
        return self.title