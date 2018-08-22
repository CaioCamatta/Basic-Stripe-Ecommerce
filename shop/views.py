from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

def index(request):
    text = ''

def allProducts(request, c_slug=None):
    c_page = None
    products_list = None

    # If there's a slug a specific category, we filter objects from that category only
    if c_slug!=None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.filter(category=c_page, available=True)
    # Else we show all products
    else:
        products_list = Product.objects.all().filter(available=True)

    # Create pagination, max 6 products/page
    paginator = Paginator(products_list, 6)

    # Try getting a page from the request
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    # Try paginating products for the specified page
    try:
        products = paginator.page(page)
    # Else go to the last page
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/category.html', {'category': c_page, 'products': products})

# Product details page
def productDetails(request, c_slug, p_slug):
    # try finding the product given the category slug and the product slug
    try:
        product = Product.objects.get(category__slug=c_slug, slug=p_slug)

    except Exception as e:
        raise e

    return render(request, 'shop/product.html', {'product':product})

def signUpView(request):
    if request.method == 'POST':
        # Assign the form data to the SignUpForm
        form = SignUpForm(request.POST)

        if form.is_valid():
            user=form.save()

            #Sign in after sign up
            if user is not None:
                login(request, user)
                return redirect('shop:allProducts')
            else:
                return redirect('signup')

            username = form.cleaned_data.get('username') # Get username
            signup_user = User.objects.get(username=username) # Find user using username
            customer_group = Group.objects.get(name='Customer') # Find Group named 'Costumer'
            customer_group.user_set.add(signup_user) # Add user to group


    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form':form})


def signInView(request):
    if request.method == 'POST':
        # Assign the form data to AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        # Authenticate user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # If authentication is correct, login and redirect to shop
        if user is not None:
            login(request, user)
            return redirect('shop:allProducts')

        else:
            return redirect('signup')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', {'form':form})

def signOutView(request):
    logout(request)
    return redirect('signin')
