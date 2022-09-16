#from django.conf import settings
from django.contrib import admin
from django.urls import path
from pay_api.views import SuccessView, CancelView, IndexView, ItemView, buy, webhook
from django.conf.urls.static import static
from pay import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('item/<int:pk>', ItemView.as_view(), name='item'),
    path('buy/<int:pk>', buy, name='buy'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhooks/stripe/', webhook, name="webhook"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

