import stripe
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from pay.settings import DOMAIN
from .models import Item

public_key = settings.STRIPE_PUBLIC_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY


class IndexView(ListView):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список товаров'
        return context

    def get_queryset(self):
        return Item.objects.all()


class ItemView(DetailView):
    model = Item
    template_name = 'item.html'
    context_object_name = 'item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs['pk'])
        context['public_key'] = settings.STRIPE_PUBLIC_KEY
        context['title'] = f"Просмотр {context['item']}"
        return context

    def get_session_id(self, **kwargs):
        item_pk = self.kwargs['pk']
        item = Item.objects.get(pk=item_pk)
        return item_pk


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


@csrf_exempt
def buy(request, pk):
    item = Item.objects.get(pk=pk)
    session = stripe.checkout.Session.create(
    client_reference_id=request.user.id if request.user.is_authenticated else None,
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': item.name,
          'description': item.description,
        },
        'unit_amount': item.price,
      },
      'quantity': 1,
    }],
    metadata={
        "order_id": item.id
    },
    mode='payment',
    success_url=DOMAIN + '/success/',
    cancel_url=DOMAIN + '/cancel/',
    )
    return JsonResponse({'id': session.id}, status=200)


@csrf_exempt
def webhook(request):
    print("Webhook")
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as exc:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as exc:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
        sessionID = session["id"]
    return HttpResponse(status=200)