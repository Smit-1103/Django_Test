from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from .forms import OrderForm, InterestForm
from .models import Category, Product, Client, Order


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    # Try to get the last login time from session
    last_login = request.session.get('last_login', None)
    # If not found, try to get it from the cookie
    if not last_login:
        last_login = request.COOKIES.get('last_login', None)

    if last_login:
        login_info = f"Your last login was: {last_login}"
    else:
        login_info = "No recent login information available."

    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'login_info': login_info})


def about(request):
    # Retrieve cookie; default to 0 if not set.
    visits = request.COOKIES.get('about_visits', 0)
    try:
        visits = int(visits) + 1
    except ValueError:
        visits = 1

    response = render(request, 'myapp/about.html', {'visits': visits})
    # Set cookie to expire in 5 minutes (300 seconds)
    response.set_cookie('about_visits', visits, max_age=300)
    return response

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})

def detail(request, cat_no):
    """ Display category details and list products under that category """
    category = get_object_or_404(Category, id=cat_no)
    products = Product.objects.filter(category=category)

    return render(request, 'myapp/detail.html', {'category': category, 'products': products})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Check stock
            if order.num_units <= order.product.stock:
                order.save()
                # Reduce stock
                order.product.stock -= order.num_units
                order.product.save()

                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()

    return render(request, 'myapp/placeorder.html', {
        'form': form,
        'msg': msg,
        'prodlist': prodlist
    })

def productdetail(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interested = int(form.cleaned_data['interested'])
            quantity = form.cleaned_data['quantity']
            comments = form.cleaned_data['comments']

            # If user is interested, increment the product’s "interested" count
            if interested == 1:
                product.interested += 1
                product.save()

            return redirect('myapp:index')  # or back to products, or wherever
    else:
        form = InterestForm()

    return render(request, 'myapp/productdetail.html', {
        'product': product,
        'form': form
    })
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # Set session expiry to 1 hour
                request.session.set_expiry(3600)
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                request.session['last_login'] = current_time
                login(request, user)
                response = HttpResponseRedirect(reverse('myapp:index'))
                # Set cookie to store last login time; for example, expire in 1 hour (3600 seconds)
                response.set_cookie('last_login', current_time, max_age=3600)
                return response
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myorders(request):
    # Check if the logged-in user is a Client.
    try:
        client = request.user
    except Client.DoesNotExist:
        return HttpResponse("You are not a registered client!")

    orders = Order.objects.filter(client=client)
    return render(request, 'myapp/myorders.html', {'orders': orders})