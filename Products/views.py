from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone


# Create your views here.
def home(request):
    product = Product.objects.all()
    return render(request, 'products/index.html', {'product': product})


@login_required(login_url='users:login')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['description'] and request.POST['url'] and request.FILES['icon'] and \
                request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.description = request.POST['description']

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']

            product.icon = request.FILES['icon']
            product.image = request.FILES['image']

            product.publish_date = timezone.datetime.now()
            product.owner = request.user
            product.save()
            return redirect('/product/' + str(product.slug) + '-' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All Fields are Required'})
    else:
        return render(request, 'products/create.html')


def detail(request, product_slug, product_id):
    product = get_object_or_404(Product, slug=product_slug, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})


@login_required(login_url='users:signup')
def likes(request, product_slug, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=product_slug, pk=product_id)
        product.total_votes += 1
        product.save()
        return redirect('/product/' + str(product.slug) + '-' + str(product.id))
