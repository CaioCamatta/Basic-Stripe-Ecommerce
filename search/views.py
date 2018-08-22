from django.shortcuts import render
from shop.models import Product
from django.db.models import Q

# Create your views here.
def searchResult(request):
    products = None
    query = None

    # query comes from the form
    if 'query' in request.GET:
        query = request.GET.get('query')
        # Filter using Q
        products = Product.objects.all().filter(Q(name__contains=query) or Q(description__contains=query))

    return render(request, 'search/search.html', {'query':query, 'products':products})
