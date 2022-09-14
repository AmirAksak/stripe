# pay>pip install --target=c:\users\lesnid\desktop\python_lessons\pay\venv\lib\site-packages --upgrade stripe
# https://raturi.in/blog/django-stripe-integration-fully-explained-example/
# https://stripe.com/docs/testing#cards

from django.shortcuts import render
import stripe
import json
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Product, Item

public_key = settings.STRIPE_PUBLIC_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = "http://127.0.0.1:8000"

def connect(id):
    item = Item.objects.get(pk=id)
    YOUR_DOMAIN = 'http://127.0.0.1:8000'
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            #payment_method_types=['card', 'affirm'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.price),
                        'product_data': {
                            'name': item.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": item.id
            },
            mode='payment',

            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        print('Checkout_Session')
        print(checkout_session)
    except Exception as exc:
        print('Ошибка', exc)


class IndexView(ListView):
    model = Item
    template_name = 'index.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Item.objects.all()


class BuyView(DetailView):
    model = Item
    template_name = 'buy.html'
    context_object_name = 'item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs['pk'])
        #context['item'] = Item.objects.get(pk=self.get_session_id())
        #connect(self.kwargs['pk'])
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
def create_checkout_session(request, pk):
    item = Item.objects.get(pk=pk)
    session = stripe.checkout.Session.create(
    client_reference_id=request.user.id if request.user.is_authenticated else None,
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': item.name,
        },
        'unit_amount': item.price,
      },
      'quantity': 1,
    }],
    metadata={
        "order_id":item.id
    },
    mode='payment',
    success_url=YOUR_DOMAIN + '/success/',
    cancel_url=YOUR_DOMAIN + '/cancel/',
    )
    print(session)
    return JsonResponse({'id': session.id})


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
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
         #creating order
        customer_email = session["customer_details"]["email"]
        price = session["amount_total"] /100
        sessionID = session["id"]
        ID=session["metadata"]["order_id"]
        #Item.objects.filter(id=ID).update(email=customer_email,amount=price,paid=True,description=sessionID)

    return HttpResponse(status=200)