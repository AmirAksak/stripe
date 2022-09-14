from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.TextField(verbose_name='Name', max_length=255, help_text='Your name', blank=False )
    description = models.TextField(verbose_name='Description', help_text='Payment description', blank=True)
    price = models.IntegerField(verbose_name='Price', help_text='Price', blank=False)

    def __str__(self):
        #return f'{self.name} / {self.price} / {self.description}'
        return self.name

    def get_dollar_price(self):
        return int(self.price / 100)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['name', 'description', 'price']

    def get_absolute_url(self):  # Ссылка на статью
        return reverse('buy', kwargs={'pk': self.pk})

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)



