
from django.shortcuts import render, redirect
from home.models import *
# from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json
import datetime
from django.db.models import Q
from django.http import JsonResponse




# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')


def contact(request):
    thank=False
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        mobile=request.POST.get('mobile', '')
        desc=request.POST.get('desc', '')
        contact = Contact(name=name, email=email, mobile=mobile, desc=desc)
        contact.save()
        thank=True
    return render(request, "contact.html", {'thank':thank})


def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request, "Username Already Exsits...")
            return redirect('/register')

        user = User.objects.create(
            username = username, 
            password = password
        )

        user.set_password(password)
        user.save()
        
        messages.success(request, "Account Created Successfully.")

        return redirect('/login')

    return render(request, 'register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login')
        
        else:
            login(request, user)
            return redirect('/buyer')

    return render(request, 'login.html')

 
def logout_page(request):
    logout(request)
    return redirect('home')
 

def search(request):
    query = request.POST.get('search')
    if len(query)>78:
        item = ItemInsert.objects.none()
    else:
        itemItem_desc= ItemInsert.objects.filter(item_desc__icontains=query)
        itemItem_group= ItemInsert.objects.filter(item_group__icontains=query)
        item= itemItem_desc.union(itemItem_group)
    if item.count() == 0:
        messages.warning(request, "No Search result found. Please refine your query ")    
    params={'item': item, 'query': query}
    return render(request, 'buyer.html', params)


#    CART VIEW
def cart(request):

    if request.user.is_authenticated:
        user_id = request.user.id
        order, created = Order.objects.get_or_create(user_id=user_id, complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    
    context = {'items':items,'order':order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    user = request.user.id
    item = ItemInsert.objects.get(id=productId)
    order , created = Order.objects.get_or_create(user = user, complete = False)

    orderItem, created= OrderItem.objects.get_or_create(order = order, item = item)
    print(action)
    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.order = order
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'message':'Item was added'}, safe=False)



def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = request.POST
    print(data)

    data = {'checkoutData':data}


    if request.user.is_authenticated:
        user_id = request.user.id
        order, created = Order.objects.get_or_create(user_id=user_id, complete=False)
        order.transaction_id = transaction_id

        order.complete = True
        order.save()

        Checkout.objects.create(
            user_id=user_id,
            orderr=order,
            
            name=data['checkoutData']['name'],
            email=data['checkoutData']['email'],
            addr=data['checkoutData']['addr'],
            city=data['checkoutData']['city'],
            state=data['checkoutData']['state'],
            zip_code=data['checkoutData']['zip_code'],
            number=data['checkoutData']['number'],
        )
    else:
        print('User is not logged in..')

    return JsonResponse({'message':'Order Placed'}, safe=False)


def buyer(request):
    item=ItemInsert.objects.all()

    query = request.GET.get('search')
    if query:
        item = ItemInsert.objects.filter(Q(item_group__icontains=query) | Q(item_desc__icontains=query) )

    return render(request, 'buyer.html',{'item':item, "usr": request.user.id})




def checkout(request):
    # print(request.POST)
    if request.user.is_authenticated:
        user_id = request.user.id
        order, created = Order.objects.get_or_create(user_id=user_id, complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
      
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False }
        cartItems = order['get_cart_items']
        
    context = {'items':items,'order':order, 'cartItems': cartItems}
        
    return render(request, "checkout.html", context)





def seller(request):
    if request.method=="POST":
        # print(request)
        image=request.FILES['image']
        item_desc=request.POST.get('item_desc', '')
        item_group=request.POST.get('item_group', '')
        # today = datetime.today()  # This works because you're importing the datetime class
        item_rate=request.POST.get('item_rate', '')
        stock_qty=request.POST.get('stock_qty', '')
        itemInsert = ItemInsert(image=image, item_desc=item_desc, item_group=item_group, item_rate=item_rate, stock_qty=stock_qty) #, item_date=datetime.today()
        itemInsert.save()
    return render(request, "seller.html") 



def update_item(request):
    if request.method == 'POST':
        # Your logic to process the POST request
        # Example response, adjust based on your logic
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

    