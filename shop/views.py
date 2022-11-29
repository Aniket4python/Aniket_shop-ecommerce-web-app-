from django.shortcuts import render,  redirect, HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import  check_password
from .models import Customer, Product, Category, Order


#home(category and cart funtion)
#showing all product to home page(by category)
#home has filter for category and [post method for add/remove product to cart 
def home(request):
    if request.method == 'GET':

        prod = None
        categories = Category.objects.all()
        categoryID = request.GET.get('category')
        your_are = request.session.get('customer_name')
        if your_are:
            print('welcom',your_are)
        else:
            print('pls login')

        if categoryID:
            prod = Product.get_all_products_by_categoryid(categoryID)
        else:
            prod = Product.objects.all()

        data = {}
        data['products'] = prod
        data['categories'] = categories

    
        return render(request, "home.html", data)
    
    #post method for adding product in cart using seassion
    product_id = request.POST.get('product')
    cart = request.session.get('cart')
    remove = request.POST.get('remove')
    if cart:
        quantity = cart.get(product_id)
        if quantity:
            if remove:
                if quantity<=1:
                    cart.pop(product_id)
                else:
                    cart[product_id]=quantity-1
            else:   
                cart[product_id]=quantity+1
        else:
            cart[product_id] = 1
    else:
        cart = {}
        cart[product_id] = 1

    request.session['cart']=cart
    return redirect('home')

#signup method(view for signup page)
def signup(request):
    #get method
    if request.method == 'GET':
        return render(request, "signup.html")
    #post method  
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('lastname')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')
       
    value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

    customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
    error_message = None

    #customer validation
    if(not first_name):
            error_message = "First Name Requried"

    elif not last_name:
            error_message = 'Last Name Required'

    elif not phone:
            error_message = 'Phone Number Required'
        
    elif len(phone)<10:
             error_message = 'Phone Number Must be !0 digit'

    elif not email:
            error_message = 'email Required'

    elif not password:
            error_message = 'Password Required'

    elif len(password)<6:
             error_message = 'Must be 6 digit'
        
    elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        
    #saving customer
    if not error_message:
            print(first_name,last_name,phone,email,password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
    data  = {
                'error':error_message,
                'values': value
            }
    return render(request, 'signup.html', data)


#login method(view for login page)
def login_page(request):
    #get method
    return_url = None
    if request.method == 'GET':
        return render(request, "login.html")
    
    #post method
    email = request.POST.get('email')
    password = request.POST.get('password')
    customer = Customer.get_customer_by_email(email)

    error_message = None

    if customer:
        flag = check_password(password, customer.password)
        
        if flag:
            request.session['customer_name'] = customer.first_name
            request.session['customer'] = customer.id #adding session for cookies
            return redirect('home')

        else:
            error_message = "Email or Password Invalid!!"

    else:
        error_message = "plase Register!!"

    return render(request, 'login.html', {'error':error_message})

def logout(request):
    request.session.clear()
    return redirect('login_page')

#faching and showing producta in cart
def cart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    print(products)
    return render(request, 'cart.html', {'products':products})

def checkout(request):
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    customer = request.session.get('customer')
    cart = request.session.get('cart')
    products = Product.get_products_by_id(list(cart.keys()))
   
    
    for product in products:
        order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
        order.save()

    request.session['cart']={}
    return redirect('cart')

def order_page(request):
    customer = request.session.get('customer')
    orders = Order.get_orders_by_customer(customer)
    print(orders)
    return render(request, 'order.html', {'orders':orders})    

