from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.TextField(verbose_name='Наименование', max_length=255, help_text='Наименование товара', blank=False )
    description = models.TextField(verbose_name='Описание', help_text='Описание товара', blank=True)
    price = models.IntegerField(verbose_name='Цена', help_text='Цена товара', blank=False)

    def __str__(self):
        return self.name

    def get_dollar_price(self):
        return '{0:.2f}'.format(self.price / 100)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', 'description', 'price']

    def get_absolute_url(self):  # Ссылка на товар при листинге
        return reverse('item', kwargs={'pk': self.pk})
