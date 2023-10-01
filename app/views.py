from django.shortcuts import render, redirect
from django.views import View
from app.models import Product, Cart, Customer, Payment, OrderPlaced, Wishlist, Product_Category
from app.encryption_util import encrypt, decrypt
from app.forms import CustomerRegistrationForm, ProfileForm
from django.contrib import messages
from django.http.response import JsonResponse
from django.db.models import Q
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
import folium


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    totalitem = 0
    totalwishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalwishlist = len(Wishlist.objects.filter(user=request.user))

    catetory = Product_Category.get_category_all().values('id', 'name').order_by('name')

    catetory1 = []
    for i in catetory:
        print('$$$$$$$$$$$$$$$$$$$$$$', i['id'])
        i['encrypt_key'] = encrypt(i['id'])
        i['id'] = i['id']
        print('#################', i['encrypt_key'])
        catetory1.append(i)
    category_id = request.GET.get('category')
    category_id1 = decrypt(category_id)
    print('!!!!!!!!!!!!!!!!!!', category_id1)
    product = []
    if category_id1:
        products = Product.get_all_product_by_category_id(category_id1)
        for i in products:
            i['encrypt_key'] = encrypt(i['id'])
            print('#@#@#@#@##@#@#@', i['encrypt_key'])
            i['id'] = i['id']
            product.append(i)
    else:
        products = Product.get_products_all().values(
            'id', 'title', 'discounted_price', 'selling_price',
            'product_image').order_by('title')
        for i in products:
            i['encrypt_key'] = encrypt(i['id'])
            print('#@#@#@#@##@#@#@', i['encrypt_key'])
            i['id'] = i['id']
            product.append(i)
    return render(request, 'home.html', locals())


@method_decorator(login_required, name='dispatch')
class Category(View):
    def get(self, request, val):
        totalitem = 0
        totalwishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            totalwishlist = len(Wishlist.objects.filter(user=request.user))
        product1 = Product.objects.values(
            'id', 'title', 'discounted_price', 'selling_price',
            'product_image').filter(category=val)
        product = []
        for i in product1:
            i['encrypt_key'] = encrypt(i['id'])
            i['id'] = i['id']
            product.append(i)
            print(i)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'category.html', locals())


@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        print('encrypted pk', pk)
        encrypted_pk = pk
        totalitem = 0
        totalwishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            totalwishlist = len(Wishlist.objects.filter(user=request.user))
        pk = decrypt(pk)
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(
            Q(product=product) & Q(user=request.user))
        return render(request, 'product_details.html', locals())


class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        totalwishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            totalwishlist = len(Wishlist.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'registration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Register Successfully')
        else:
            messages.error(request, 'invalid data input')
        return render(request, 'registration.html', locals())


@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):
        totalitem = 0
        totalwishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            totalwishlist = len(Wishlist.objects.filter(user=request.user))
        form = ProfileForm()
        return render(request, 'profile.html', locals())

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']
            cust = Customer(user=user, name=name, locality=locality,
                            city=city, state=state, mobile=mobile, zipcode=zipcode)
            cust.save()
            messages.success(
                request, 'Congratulations! Profile Saved Successfully')
        else:
            messages.warning(request, 'Invalid Input Entered')
        return render(request, 'profile.html', locals())


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def address(request):
    totalitem = 0
    totalwishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalwishlist = len(Wishlist.objects.filter(user=request.user))
    custadd = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', locals())


@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        totalitem = 0
        totalwishlist = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            totalwishlist = len(Wishlist.objects.filter(user=request.user))
        cust = Customer.objects.get(pk=pk)
        form = ProfileForm(instance=cust)
        return render(request, 'addressUpdate.html', locals())

    def post(self, request, pk):
        form = ProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.mobile = form.cleaned_data['mobile']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Updated Successfully')
        else:
            messages.warning(request, 'Invalid Data')
        return redirect('address')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_to_cart(request):
    totalitem = 0
    totalwishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalwishlist = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    print("--------------", product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('showcart')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showcart(request):
    totalitem = 0
    totalwishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalwishlist = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for i in cart:
        value = i.quantity * i.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    print("----------", totalamount)
    return render(request, 'addtocart.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        pid = request.GET['prod_id']
        print(pid)
        c = Cart.objects.get(Q(product=pid) & Q(user=request.user))
        c.quantity += 1
        c.save()
        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        pid = request.GET['prod_id']
        print(pid)
        c = Cart.objects.get(Q(product=pid) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        pid = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=pid) & Q(user=request.user))
        c.delete()
        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        amount = 0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, 'currency': 'INR',
                'receipt': 'order_rcptid_12'}
        payment_response = client.order.create(data=data)
        print('payment res-----------------', payment_response)
        # {'id': 'order_Mf3aWiePDGPtge', 'entity': 'order', 'amount': 8500, 'amount_paid': 0, 'amount_due': 8500, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1695314887}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(user=user, amount=totalamount, razorpay_order_id=order_id,
                              razorpay_payment_status=order_status)
            payment.save()
        return render(request, 'checkout.html', locals())


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def paymentdone(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    print('=============', cust_id, order_id, payment_id)
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product,
                    quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect('/orders')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def orders(request):
    totalitem = 0
    totalwishlist = 0
    user = request.user
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalwishlist = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', locals())


def plus_wishlist(request):
    if request.method == 'GET':
        user = request.user
        pid = request.GET['prod_id']
        pk = decrypt(pid)
        product = Product.objects.get(id=pk)
        Wishlist(user=user, product=product).save()

        data = {
            'message': 'Wishlist Added sucessfully'
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        user = request.user
        pid = request.GET['prod_id']
        pk = decrypt(pid)
        print('product id', pk)
        product = Product.objects.get(id=pk)
        print('================', product)
        Wishlist.objects.filter(user=user, product=product).delete()

        data = {
            'message': 'Wishlist Deleted sucessfully'
        }
        return JsonResponse(data)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    search = request.GET['search']
    totalitem = 0
    totalwishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalwishlist = len(Wishlist.objects.filter(user=request.user))
    # product1 = Product.objects.filter(Q(title__icontains=search))

    product1 = Product.objects.values(
        'id', 'title', 'discounted_price', 'selling_price',
        'product_image').filter(Q(title__icontains=search))
    product = []
    for i in product1:
        i['encrypt_key'] = encrypt(i['id'])
        i['id'] = i['id']
        product.append(i)
    return render(request, 'search.html', locals())


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def wishlist(request):
    totalitem = 0
    totalwishlist = 0
    user = request.user
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        totalwishlist = len(Wishlist.objects.filter(user=request.user))

    wishlist = Wishlist.objects.filter(user=user)
    for i in wishlist:
        print('7777777777777777777', type(i))

    product = []
    for i in wishlist:
        i.encrypt_id = encrypt(i.product.pk)
        i.pk = i.pk
        product.append(i)
    return render(request, 'wishlist.html', locals())


def about(request):
    m = folium.Map(location=[17.627038, 81.051283], zoom_start=13)
    folium.Marker(location=[17.627038, 81.051283],
                  tooltip='Click for more', popup='Sri Sai Ram Readymades \n Contact No 9959171018').add_to(m)
    # m = folium.Map()
    m = m._repr_html_()

    folium.raster_layers.TileLayer()

    return render(request, 'about.html', locals())
