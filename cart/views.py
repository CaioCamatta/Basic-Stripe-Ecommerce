from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from order.models import Order, OrderItem
from django.template.loader import get_template
from django.core.mail import EmailMessage

# Helper function to get the cart ID
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart=request.session.create()

    return cart

# Add product to car
def add_cart_item(request, product_id):
    product = Product.objects.get(id=product_id)

    # Find/create the cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    # Increase amount of selected product in the cart if there's enough stock
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()

    # If the item is not already in the cart, create it
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()

    return redirect('cart:cart_detail')

# Cart detail page
def cart_detail(request, total=0, counter=0, cart_items = None):
    # Get cart, subtotals, quantities
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    # STRIPE INTEGRATION
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total*100)
    description = "Stripe Tutorial - New Order"
    publishable_key = settings.STRIPE_PUBLISHABLE_KEY

    # When the form is received
    if request.method == 'POST':
        try:
            # Get info
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']

            # Billing
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostCode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']

            # Shipping
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostCode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']

            # Create stripe costumer
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            # Create charge
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )

            # Create the order
            try:
                # Use form data to fill Order model
                order_details = Order.objects.create(
                    token=token,
                    total=total,
					emailAddress = email,
					billingName = billingName,
					billingAddress1 = billingAddress1,
					billingCity = billingCity,
					billingPostCode = billingPostCode,
					billingCountry = billingCountry,
					shippingName = shippingName,
					shippingAddress1 = shippingAddress1,
					shippingCity = shippingCity,
					shippingPostCode = shippingPostCode,
					shippingCountry = shippingCountry
                )
                order_details.save()

                # Add items to the order
                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                        product = order_item.product.name,
                        quantity = order_item.quantity,
                        price = order_item.product.price,
                        order = order_details
                    )
                    oi.save()

                    # Remove the products bought from stock
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()

                    # Delete product from cart
                    order_item.delete()
                    print('Order Created.')

                # Try sending email to costumer about the order
                try:
                    sendEmail(order_details.id)
                    print('Order email sent.')

                except IOError as e:
                    print(e)
                    return e

                return redirect('order:thanks', order_details.id)

            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
          # Since it's a decline, stripe.error.CardError will be caught
            print(e)
            return False, e
        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          pass
        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          pass
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          pass
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          pass
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          pass
        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          pass

    return render(request, 'cart/cart.html', dict(cart_items=cart_items, total=total, counter=counter, publishable_key=publishable_key, stripe_total=stripe_total, description=description))

# - 1 item
def item_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect('cart:cart_detail')

# Delete item (regardless of amount) from cart
def item_full_delete(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    # Delete item
    cart_item.delete()

    return redirect('cart:cart_detail')

def sendEmail(order_id):
    # Use order id to get the Order object and the OrderItems
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)

    try:
        # Sending order to costumer
        subject = "Perfect Cushion Store - New Order #{}".format(transaction.id)
        to = ['{}'.format(transaction.emailAddress)]
        from_email = 'orders@perfectcushionstore.com'
        order_info = {
            'trasaction': transaction,
            'order_items': order_items
        }
        message = get_template('email/email.html').render(order_info) # Render html template with order_info context
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    except IOError as e:
        print(e)
        return e
