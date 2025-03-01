from django.shortcuts import render, get_object_or_404, redirect

from .forms import OrderForm, InterestForm
from .models import Category, Product, Order

def index(request):
    """ Main landing page displaying categories & top 5 expensive products """
    cat_list = Category.objects.all().order_by('id')[:10]  # Fetch first 10 categories
    product_list = Product.objects.all().order_by('-price')[:5]  # Get top 5 expensive products
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'product_list': product_list})

def about(request):
    """ Renders the About Us page """
    return render(request, 'myapp/about.html')

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
    prodlist = Product.objects.all()  # optional, if you want to display on the page

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

from django.shortcuts import get_object_or_404, redirect

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

            # You might choose to do something with quantity or comments here as well,
            # such as logging or storing them.

            return redirect('myapp:index')  # or back to products, or wherever
    else:
        form = InterestForm()

    return render(request, 'myapp/productdetail.html', {
        'product': product,
        'form': form
    })
