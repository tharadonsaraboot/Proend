def get_cart(request):
    """Retrieve the cart from session"""
    cart = request.session.get('cart', {})
    return cart

def add_to_cart(request, product_id, quantity):
    """Add a product to the cart or update its quantity."""
    cart = get_cart(request)
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)  # Convert to string if your session stores keys as strings
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True  # Make sure to mark the session as "modified" to save it


def clear_cart(request):
    """Remove all items from the cart."""
    request.session['cart'] = {}