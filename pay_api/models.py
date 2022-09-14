from django.db import models


class Item(models.Model):
    name = models.TextField(verbose_name='Name', max_length=255, help_text='Your name', blank=False )
    description = models.TextField(verbose_name='Description', help_text='Payment description', blank=True)
    price = models.FloatField(verbose_name='Price', help_text='Price', blank=False)

    def __str__(self):
        #return f'{self.name} / {self.price} / {self.description}'
        return self.name

    class Meta:
        verbose_name = 'Payer'
        verbose_name_plural = 'Payers'
        ordering = ['name', 'description', 'price']


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)



