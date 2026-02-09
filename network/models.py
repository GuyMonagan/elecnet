from django.db import models
from decimal import Decimal


class BusinessUnit(models.Model):
    name = models.CharField(max_length=255)

    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)

    debt_to_supplier = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Задолженность поставщику"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients'
    )

    def __str__(self):
        return f'{self.name} — {self.city}'

    def get_level(self):
        level = 0
        current = self.supplier
        while current:
            level += 1
            current = current.supplier
        return level


class Product(models.Model):
    owner = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return f'{self.name} ({self.model})'
