from django.db import models
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Expense(models.Model):
    title = models.CharField(max_length=120)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    category = models.CharField(max_length=50, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'{self.title} ({self.amount})'