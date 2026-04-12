# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Category, Product
# from django.contrib import messages
# from django.db import migrations

# # Create your views here.

# @login_required(login_url='login_page')
# def home(request):
#     if not request.session.get('user_id'):
#         return redirect('login')

#     products = Product.objects.all()
#     return render(request, 'products.html', {'products': products})


# @login_required(login_url='login_page')
# def add_product(request):

#     # ✅ login check
#     if not request.session.get('user_id'):
#         return redirect('login')

#     # ✅ admin check
#     if request.session.get('role') != 'admin':
#         messages.error(request, "Access Denied ❌")
#         return redirect('home')

#     categories = Category.objects.all()

#     if request.method == "POST":
#         name = request.POST.get('name')
#         price = request.POST.get('price')
#         image = request.POST.get('image')
#         category_id = request.POST.get('category')

#         category = Category.objects.get(id=category_id)

#         Product.objects.create(
#             name=name,
#             price=price,
#             vechicle_image=image,
#             category=category
#         )

#         messages.success(request, "Product Added Successfully ✅")
#         return redirect('home')

#     return render(request, 'add_product.html', {'categories': categories})



# @login_required(login_url='login_page')
# def edit_product(request, id):

#     if request.user.role != 'admin':
#         messages.error(request, "Access Denied ❌")
#         return redirect('home')

#     product = Product.objects.get(id=id)
#     categories = Category.objects.all()

#     if request.method == "POST":
#         product.name = request.POST.get('name')
#         product.price = request.POST.get('price')
#         product.vechicle_image = request.POST.get('image')

#         category_id = request.POST.get('category')
#         product.category = Category.objects.get(id=category_id)

#         product.save()

#         messages.success(request, "Product Updated ✅")
#         return redirect('home')

#     return render(request, 'add_product.html', {
#         'product': product,
#         'categories': categories
#     })
    
# @login_required(login_url='login_page')
# def delete_product(request, id):

#     if request.user.role != 'admin':
#         messages.error(request, "Access Denied ❌")
#         return redirect('home')

#     if request.method == "POST":
#         product = Product.objects.get(id=id)
#         product.delete()
#         messages.success(request, "Product Deleted 🗑️")

#     return redirect('home')

# def about(request):
#     return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')

# def add_to_cart(request, id):

#     if not request.user.is_authenticated:
#         messages.error(request, "⚠️ Please login first to add items to cart!")
#         return redirect('login_page')

#     if request.method == "POST":
#         cart = request.session.get('cart', {})

#         cart[str(id)] = cart.get(str(id), 0) + 1

#         request.session['cart'] = cart
#         messages.success(request, "✅ Product added to cart successfully!")

#     # ✅ Safe redirect
#     return redirect(request.META.get('HTTP_REFERER') or 'home')

    
# def cart_view(request):
#     cart = request.session.get('cart', {})
#     products = []
#     total = 0

#     for id, qty in cart.items():

#         try:
#             product = Product.objects.get(id=id)
#         except Product.DoesNotExist:
#             continue  # ✅ skip deleted product

#         # ✅ Assuming price stored as IntegerField
#         price = product.price

#         product.qty = qty
#         product.total_price = price * qty

#         total += product.total_price
#         products.append(product)

#     return render(request, 'cart.html', {
#         'products': products,
#         'total': total
#     })


# def remove_from_cart(request, id):
#     cart = request.session.get('cart', {})

#     if str(id) in cart:
#         del cart[str(id)]

#     request.session['cart'] = cart
#     messages.success(request, "🗑️ Item removed from cart")

#     return redirect('cart')

from django.shortcuts import render, redirect
from .models import Category, Product
from django.contrib import messages


# ================= HOME =================
def home(request):
    if not request.session.get('user_id'):
        return redirect('login')

    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


# ================= ADD PRODUCT =================
def add_product(request):

    if not request.session.get('user_id'):
        return redirect('login')

    if request.session.get('role') != 'admin':
        messages.error(request, "Access Denied ❌")
        return redirect('home')

    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        image = request.POST.get('image')
        category_id = request.POST.get('category')

        category = Category.objects.get(id=category_id)

        Product.objects.create(
            name=name,
            price=price,
            vechicle_image=image,
            category=category
        )

        messages.success(request, "Product Added Successfully ✅")
        return redirect('home')

    return render(request, 'add_product.html', {'categories': categories})


# ================= EDIT PRODUCT =================
def edit_product(request, id):

    if not request.session.get('user_id'):
        return redirect('login')

    if request.session.get('role') != 'admin':
        messages.error(request, "Access Denied ❌")
        return redirect('home')

    product = Product.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.vechicle_image = request.POST.get('image')

        category_id = request.POST.get('category')
        product.category = Category.objects.get(id=category_id)

        product.save()
        messages.success(request, "Product Updated ✅")
        return redirect('home')

    return render(request, 'add_product.html', {
        'product': product,
        'categories': categories
    })


# ================= DELETE PRODUCT =================
def delete_product(request, id):

    if not request.session.get('user_id'):
        return redirect('login')

    if request.session.get('role') != 'admin':
        messages.error(request, "Access Denied ❌")
        return redirect('home')

    if request.method == "POST":
        product = Product.objects.get(id=id)
        product.delete()
        messages.success(request, "Product Deleted 🗑️")

    return redirect('home')


# ================= OTHER PAGES =================
def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# ================= CART =================
def add_to_cart(request, id):

    if not request.session.get('user_id'):
        messages.error(request, "⚠️ Please login first!")
        return redirect('login')

    if request.method == "POST":
        cart = request.session.get('cart', {})
        cart[str(id)] = cart.get(str(id), 0) + 1
        request.session['cart'] = cart

        messages.success(request, "✅ Product added to cart!")

    return redirect(request.META.get('HTTP_REFERER') or 'home')


def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, qty in cart.items():

        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            continue

        # ✅ FIX HERE
        price = int(product.price)

        product.qty = qty
        product.total_price = price * qty

        total += product.total_price
        products.append(product)

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    messages.success(request, "🗑️ Item removed")

    return redirect('cart')