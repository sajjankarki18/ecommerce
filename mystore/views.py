from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import *
from django.http import JsonResponse
import json
import datetime

# Create your views here.

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(
            customer = customer,
            complete = False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        cart_items = order['get_cart_items']
    
    products = Product.objects.all()
    context = {'products': products, 'items': items, 'cart_items': cart_items, 'shipping': False}

    return render(request, 'store.html', context)

def cart(request):
    if request.user.is_authenticated: #checks weather the user is authenticated to the site
        customer = request.user.customer #retrieves the logged user

        order, created = Order.objects.get_or_create( #creates an order object with the retreived customer
            customer = customer,
            complete = False
        )
        items = order.orderitem_set.all() #retrives all the order related information
        cart_items = order.get_cart_items
    else:
        items = [] #if user is not logged in lists returns empty
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order,  'cart_items': cart_items, 'shipping': False}        
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated: #checks weather the user is authenticated to the site
        customer = request.user.customer #retrieves the logged user

        order, created = Order.objects.get_or_create( #creates an order object with the retreived customer
            customer = customer,
            complete = False
        )
        items = order.orderitem_set.all() #retrives all the order related information
        cart_items = order.get_cart_items
    else:
        items = [] #if user is not logged in lists returns empty
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order,  'cart_items': cart_items, 'shipping': False}     
    return render(request, 'checkout.html', context)

def updateOrder(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
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
        customer = request.user.customer
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




