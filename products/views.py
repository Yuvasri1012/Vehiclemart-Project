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
        try:                                          # ← 8 spaces indent
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('image')   # ✅ FILES use பண்ணு
            category_id = request.POST.get('category')
            
            category = Category.objects.get(id=category_id)

            Product.objects.create(
            name=name,
            price=price,
            vechicle_image=image,            # ✅ file object directly
            category=category
            )

            messages.success(request, "Product Added Successfully ✅")
            return redirect('home')

        except Exception as e:
            print("ERROR:", e)
            messages.error(request, f"Error: {e}")

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

        image = request.FILES.get('image')  # ✅ POST block-ல் மட்டும்
        if image:
            product.vechicle_image = image

        category_id = request.POST.get('category')
        product.category = Category.objects.get(id=category_id)

        product.save()
        messages.success(request, "Product Updated ✅")
        return redirect('home')

    # ✅ GET request — இங்க image variable இல்லாம directly render
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