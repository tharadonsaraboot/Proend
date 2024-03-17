from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.models import Notification
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.utils.cart import get_cart
from products.models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentSlipForm
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    cart = get_cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(**form.cleaned_data, user=request.user)
            for item_id, quantity in cart.items():
                product = Product.objects.get(id=item_id)
                OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
            # Clear the cart
            request.session['cart'] = {}
            return redirect('upload_payment_slip', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'orders/checkout.html', {'form': form})

def upload_payment_slip(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Calculate the total price for the order
    total_price = sum(item.product.price * item.quantity for item in order.items.all())
    
    if hasattr(order, 'payment_slip'):
        # Handle the situation - you can redirect, show an error message, etc.
        return render(request, 'orders/payment_slip_error.html', {
            'message': 'A payment slip has already been uploaded for this order.',
            'order': order,
            'total_price': total_price
        })

    if request.method == 'POST':
        form = PaymentSlipForm(request.POST, request.FILES)
        if form.is_valid():
            payment_slip = form.save(commit=False)
            payment_slip.order = order
            payment_slip.save()
            return redirect('payment_confirmation', order_id=order_id)
    else:
        form = PaymentSlipForm()
        
    # Pass the total price to the template
    return render(request, 'orders/upload_slip.html', {
        'form': form,
        'order': order,
        'total_price': total_price
    })

def payment_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'message': 'We have received your payment slip and are currently processing your order.'
    }
    return render(request, 'orders/payment_confirmation.html', context)

def pending_payments(request):
    pending_orders = Order.objects.filter(status='pending')
    return render(request, 'orders/pending_payments.html', {'pending_orders': pending_orders})