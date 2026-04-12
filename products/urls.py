from django.urls import path
from .views import home, add_product, edit_product, delete_product, about, contact,add_to_cart,cart_view,remove_from_cart

urlpatterns = [
    # Home
    path('home/', home, name='home'),

    # Product CRUD
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('delete-product/<int:id>/', delete_product, name='delete_product'),

    # Cart
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', remove_from_cart, name='remove_from_cart'),

    # Static pages
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]