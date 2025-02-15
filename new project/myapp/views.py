from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def index(request):
    """ Main landing page displaying categories & top 5 expensive products """
    cat_list = Category.objects.all().order_by('id')[:10]  # Fetch first 10 categories
    product_list = Product.objects.all().order_by('-price')[:5]  # Get top 5 expensive products

    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'product_list': product_list})

def about(request):
    """ Renders the About Us page """
    return render(request, 'myapp/about.html')


def detail(request, cat_no):
    """ Display category details and list products under that category """
    category = get_object_or_404(Category, id=cat_no)
    products = Product.objects.filter(category=category)

    return render(request, 'myapp/detail.html', {'category': category, 'products': products})
