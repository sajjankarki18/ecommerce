from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime
from .import auth_views
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='loginUser')
def store(request):

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)

        order, created = Order.objects.get_or_create(
            customer = customer,
            complete = False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        cart_items = 0
        order = None  # Initialize order to None for unauthenticated users

    products = Product.objects.all()
    context = {'products': products, 'items': items, 'cart_items': cart_items, 'shipping': False, 'order': order}

    return render(request, 'store.html', context)

def get_searched_product(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains = query)

    return render(request, 'store.html', {'products': products})

@login_required(login_url='loginUser')
def cart(request):
    if request.user.is_authenticated: #checks weather the user is authenticated to the site
        customer, created = Customer.objects.get_or_create(user=request.user)

        order, created = Order.objects.get_or_create( #creates an order object with the retreived customer
            customer = customer,
            complete = False
        )
        items = order.orderitem_set.all() #retrives all the order related information
        cart_items = order.get_cart_items
    else:
        items = []
        cart_items = 0
        order = None  # Initialize order to None for unauthenticated users

    context = {'items': items, 'order': order,  'cart_items': cart_items, 'shipping': False}        
    return render(request, 'cart.html', context)

@login_required(login_url='loginUser')
def checkout(request):
    if request.user.is_authenticated: #checks weather the user is authenticated to the site
        customer, created = Customer.objects.get_or_create(user=request.user)

        order, created = Order.objects.get_or_create( #creates an order object with the retreived customer
            customer = customer,
            complete = False
        )
        items = order.orderitem_set.all() #retrives all the order related information
        cart_items = order.get_cart_items
    else:
        items = []
        cart_items = 0
        order = None  # Initialize order to None for unauthenticated users

    context = {'items': items, 'order': order,  'cart_items': cart_items, 'shipping': False}     
    return render(request, 'checkout.html', context)

def updateOrder(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer, created = Customer.objects.get_or_create(user=request.user)
    product = Product.objects.get(id = productId)

    order, created = Order.objects.get_or_create(
        customer = customer,
        complete = False
    )

    orderItems, created = OrderItem.objects.get_or_create(
        order = order,
        product = product
    )

    if action == 'add':
        orderItems.quantity = (orderItems.quantity + 1)
    elif action == 'remove':
        orderItems.quantity = (orderItems.quantity - 1)

    orderItems.save()

    if orderItems.quantity <= 0:
        orderItems.delete()

    return JsonResponse('the cart has been updated!', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(
            customer = customer,
            complete = False
        )

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('The user is not logged in!')            

    return JsonResponse('the order has been completed!', safe=False)




