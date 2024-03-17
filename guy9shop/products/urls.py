from django.urls import path
from products.views import product_list 

urlpatterns = [
    # your other url patterns
    path('', product_list, name='product_list'),
]
