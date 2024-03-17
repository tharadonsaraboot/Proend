from django.shortcuts import render, redirect
from .utils.cart import get_cart, add_to_cart, remove_from_cart
from products.models import Product
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def cart_detail(request):
    cart = get_cart(request)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    
    total_price = sum(product.price * quantity for product_id, quantity in cart.items() for product in products if product.id == int(product_id))

    return render(request, 'cart/detail.html', {
        'cart': cart,
        'products': products,
        'total_price': total_price,
    })

def add_to_cart_view(request, product_id):
    quantity = request.POST.get('quantity', 1)  # Default to 1 if not provided
    add_to_cart(request, product_id, int(quantity))
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    remove_from_cart(request, product_id)
    return redirect('cart_detail')

@require_POST
def increase_quantity(request, product_id):
    # Get the current quantity for the product from the cart
    cart = get_cart(request)
    current_quantity = cart.get(str(product_id), 0)
    
    # Increase the quantity
    new_quantity = current_quantity + 1
    
    # Call add_to_cart with the new quantity
    add_to_cart(request, product_id, new_quantity)
    
    # Make sure the session is saved
    request.session.modified = True
    
    # Return the new quantity in the JsonResponse
    return JsonResponse({'quantity': new_quantity})

@require_POST
def decrease_quantity(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)  # Convert to string if your session stores keys as strings
    
    # If the product is in the cart and its quantity is greater than 1, decrease it
    if cart.get(product_id_str, 0) > 1:
        cart[product_id_str] -= 1
    # If the quantity is 1 or less, remove the item from the cart
    elif cart.get(product_id_str, 0) == 1:
        cart.pop(product_id_str, None)
    
    # Update the session cart
    request.session['cart'] = cart
    request.session.modified = True  # Make sure to save the session changes
    
    # Return the new quantity, or that the item has been removed
    new_quantity = cart.get(product_id_str, 0)
    return JsonResponse({'quantity': new_quantity})