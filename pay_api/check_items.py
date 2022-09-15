from pay.settings import STATICFILES_DIRS
from pay_api.models import Item


def check_items(): # Если нет товаров в базе, заполним из файла
    if not Item.objects.count():
        with open(STATICFILES_DIRS[0] + '\\csv\\insert.csv') as f:
            for i in range(5):
                item = Item(
                    name=f.readline(),
                    description=f.readline(),
                    price=f.readline()
                )
                item.save()