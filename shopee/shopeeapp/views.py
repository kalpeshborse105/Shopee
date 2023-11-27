from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from shopeeapp.models import Index, Customer, Cart, Order, Orderhistory
import random
from django.db.models import Q
import razorpay
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db import transaction

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    context = {}
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        ue = request.POST['uname']
        upas = request.POST['upwrd']
        fn = request.POST['fn']
        ln = request.POST['ln']
        mb = request.POST['mobile']
        ct = request.POST['city']
        pin = request.POST['pin']
        if ue == '' or upas == '':
            context['errmsg'] = "Fields cannot be empty!!"
            return render(request, 'register.html', context)
        elif len(upas) < 6:
            context['errmsg'] = "Password must be at least 6 characters"
            return render(request, 'register.html', context)
        else:
            try:
                u = User.objects.create(username=ue, email=ue)
                u.set_password(upas)
                u.save()
                c = Customer.objects.create(user=u, fn=fn, ln=ln, mobno=mb, city=ct, pincode=pin)
                c.save()
                context['success'] = "User created successfully"
                return redirect('/login', context)
            except Exception:
                existing_user = User.objects.get(username=ue)
                c = Customer.objects.create(user=existing_user, fn=fn, ln=ln, mobno=mb, city=ct, pincode=pin)
                c.save()
                context['errmsg'] = "User with the same username already exists. Please login."
                return render(request, 'register.html', context)

def user_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        name = request.POST['uname']
        upas = request.POST['upwrd']
        u = authenticate(username=name, password=upas)
        if u is not None:
            login(request, u)
            return redirect('/index')
        else:
            context = {}
            context['errmsg'] = "Invalid username and password"
            return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    return redirect('/login')

def catfilter(request, cv):
    q1 = Q(is_active=True)
    q2 = Q(cat=cv)
    p = Index.objects.filter(q1 & q2)
    context = {}
    context['data'] = p
    return render(request, 'index.html', context)

def sortprice(request, sv):
    if sv == '1':
        t = '-oprice'
    else:
        t = 'oprice'
    p = Index.objects.order_by(t).filter(is_active=True)
    context = {}
    context['data'] = p
    return render(request, 'index.html', context)

def pricefilter(request):
    min_price = request.GET['min']
    max_price = request.GET['max']
    q1 = Q(oprice__gte=min_price)
    q2 = Q(oprice__lte=max_price)
    p = Index.objects.filter(q1 & q2)
    context = {}
    context['data'] = p
    return render(request, 'index.html', context)

def index(request):
    p = Index.objects.filter(is_active=True)
    
    context = {}
    context['data'] = p
    return render(request, 'index.html', context)

def cart(request, pid):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        product = Index.objects.get(id=pid)
        cart_item = Cart.objects.filter(userid=user, pid=product).first()

        success = ""
        msg = ""

        if cart_item:
            msg = "Product already exists in cart"
        else:
            cart_item = Cart(userid=user, pid=product)
            cart_item.save()
            success = "Product added successfully to cart"

        context = {
            'msg': msg,
            'success': success,
            'data': [product],
        }
        return render(request, 'laptop_detail.html', context)
    else:
        return redirect('/login')

def laptop_detail(request, pid):
    p = Index.objects.filter(id=pid)
    context = {}
    context['data'] = p
    return render(request, 'laptop_detail.html', context)

def placeorder(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        cart_items = Cart.objects.filter(userid=user)
        orderid = random.randrange(10051995, 19950510)
        date = timezone.now().date()

        with transaction.atomic():
            for item in cart_items:
                amount = item.qty * item.pid.oprice
                order = Order.objects.create(orderid=orderid, qty=item.qty, pid=item.pid, userid=user, amt=amount, date=date)
                Orderhistory.objects.create(userid=user, orderid=order, pid=item.pid, qty=item.qty, amt=amount, date=date)

            cart_items.delete()

        return redirect('/fetchorder')
    else:
        return redirect('/login')

def fetchorderdetails(request):
    if request.user.is_authenticated:
        user_data = User.objects.get(id=request.user.id)
        customer_data = Customer.objects.filter(user=user_data)
        orders = Order.objects.filter(userid=user_data)
        total_amount = sum(order.amt for order in orders)

        context = {
            'orders': orders,
            'tamount': total_amount,
            'n': len(orders),
            'user_data': user_data,
            'customer_data': customer_data,
        }
        return render(request, 'order.html', context)
    else:
        return redirect('/login')

def viewcart(request):
    if request.user.is_authenticated:
        user_data = User.objects.get(id=request.user.id)
        customer_data = Customer.objects.filter(user=user_data)
        cart_items = Cart.objects.filter(userid=user_data)
        total = 0

        for item in cart_items:
            item.total_price = item.pid.oprice * item.qty
            total += item.total_price

        context = {
            'data': cart_items,
            'total': total,
            'n': len(cart_items),
            'user_data': user_data,
            'customer_data': customer_data,
        }
        return render(request, 'cart.html', context)
    else:
        return redirect('/login')

def updateqty(request, x, cid):
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(id=cid)
        qty = cart_item.qty

        if x == '1':
            qty += 1
        elif qty > 1:
            qty -= 1

        cart_item.qty = qty
        cart_item.save()

        return redirect('/viewcart')

def removecart(request, cid):
    if request.user.is_authenticated:
       cart_item = Cart.objects.get(id=cid)
       cart_item.delete()
       return redirect('/viewcart')

def removeorder(request, cid):
    if request.user.is_authenticated:
        order = Order.objects.get(id=cid)
        order.delete()

        return redirect('/fetchorder')

def makepayment(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        orders = Order.objects.filter(userid=user)
        total_amount = sum(order.amt for order in orders)
        orderid = random.randrange(1000000, 9999999)

        client = razorpay.Client(auth=("rzp_test_zcP5QlKsXgV1N8", "R20GqnoEJVZKwFZgk9PEQa1T"))
        payment_data = {
            "amount": total_amount * 100,
            "currency": "INR",
            "receipt": str(orderid),
        }
        payment = client.order.create(data=payment_data)

        context = {
            'payment': payment,
            'amount': total_amount,
        }
        return render(request, 'pay.html', context)
    else:
        return redirect('/login')

def generate_invoice_pdf(html):
    template = get_template('invoice.html')
    rendered_html = template.render(html)
    pdf_file = BytesIO()

    pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_file)

    pdf_file.seek(0)
    pdf_content = pdf_file.getvalue()
    pdf_file.close()

    if pisa_status.err:
        return None

    return pdf_content

def invoice_download(request, orderid):
    order = Order.objects.get(id=orderid)
    tamount = order.amt

    html = {'order': order, 'tamount': tamount}
    pdf = generate_invoice_pdf(html)

    if pdf:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=invoice_{order.orderid}.pdf'
        response.write(pdf)
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)



def paymentsuccess(request):
    sub = "Ekart-Order Status"
    frm = "noreply@LaptopStore.com"
    to = request.user.email

    order = Order.objects.filter(userid=request.user.id).latest('date')
    tamount = order.amt

    html = {'order': order, 'tamount': tamount}
    pdf_content = generate_invoice_pdf(html)

    if pdf_content is None:
        
        return HttpResponse("Error generating PDF", status=500)

    email = EmailMultiAlternatives(sub, '', frm, [to])
    email.attach('invoice.pdf', pdf_content, 'application/pdf')
    email.send()

    context = {}
    return render(request, 'paymentsuccess.html', context)


# @login_required
def dashboard(request):
    if request.user.is_authenticated:
        user_data = User.objects.get(id=request.user.id)
        customer_data = Customer.objects.filter(user=user_data)

        context = {
            'user_data': user_data,
            'customer_data': customer_data,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/login')

@login_required
def update(request):
    context = {}
    if request.method == "GET":
        user_data = User.objects.get(id=request.user.id)
        customer_data = Customer.objects.get(user=user_data)

        context = {
            'user_data': user_data,
            'customer_data': customer_data,
        }
        return render(request, 'edit.html', context)
    elif request.method == "POST":
        user_data = User.objects.get(id=request.user.id)
        customer_data = Customer.objects.get(user=user_data)
        fn = request.POST['fn']
        ln = request.POST['ln']
        mb = request.POST['mobile']
        ct = request.POST['city']
        pin = request.POST['pin']

        customer_data.fn = fn
        customer_data.ln = ln
        customer_data.mobno = mb
        customer_data.city = ct
        customer_data.pincode = pin
        customer_data.save()

        context['success'] = "User Updated successfully"
        return redirect('/dashboard', context)

            
def orderhistory(request, cid):
    if request.user.is_authenticated:
        user = User.objects.get(id=cid)
        order_history = Orderhistory.objects.filter(userid=user)

        context = {
            'order_history': order_history,
        }
        return render(request, 'orderhistory.html', context)
    else:
        return redirect('/login')

