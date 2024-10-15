from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from .models import ContactMessage
from django.core.mail import send_mail


def index(request):
    template = loader.get_template('index.html')
    
    return HttpResponse(template.render({'user':request.user}))

def about(request):
    template = loader.get_template('about.html')
    
    return HttpResponse(template.render())

def cart(request):
    if request.method == 'POST':
       
        cart = request.session.get('cart', {})
        
        
        for product_id in list(cart.keys()):
            remove_key = f'remove_{product_id}'
            quantity_key = f'quantity_{product_id}'
            
            if remove_key in request.POST:
                
                del cart[product_id]
            elif quantity_key in request.POST:
                
                quantity_str = request.POST.get(quantity_key)
                try:
                    quantity = int(quantity_str)
                    if quantity > 0:
                        cart[product_id]['quantity'] = quantity
                    else:
                        
                        del cart[product_id]
                except ValueError:
                    
                    pass
        
        
        request.session['cart'] = cart
        
        return redirect('mycart')  

    else:
       
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = 0.0 

        for product_id, item in cart.items():
            try:
                price = float(item['price'])  
            except (ValueError, TypeError):
                price = 0.0  

            subtotal = price * item['quantity']
            total_price += subtotal
            cart_items.append({
                'id': product_id,
                'name': item['name'],
                'price': price,
                'quantity': item['quantity'],
                'image': item['image'],
                'subtotal': subtotal,
            })

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, 'cart.html', context)




def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        
        contact_message = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        contact_message.save() 

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact') 

    return render(request, 'contact.html')  

    
def shop(request):
    categories = Category.objects.all()

    
    selected_category = request.GET.get('category')

    
    if selected_category and selected_category.lower() != 'all':
        products = Product.objects.filter(category__name__iexact=selected_category)
    else:
        products = Product.objects.all()

    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }

    
    return render(request, 'shop.html', context)

def product(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }
    return render(request, 'product.html', context)


def add_to_cart(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    
    
    cart = request.session.get('cart', {})
    
    product_id_str = str(product.id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.primary_image.url,
        }
    
    
    request.session['cart'] = cart
    
    return redirect('mycart')

def place_order(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    if request.method == 'POST':
        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect('mycart')

        fname = request.POST.get('fname')
        lname = request.POST.get('last')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        kebele = request.POST.get('kebele')
        note = request.POST.get('note')

        total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

        
        order = Order.objects.create(
            customer_name=fname,
            customer_last=lname,
            customer_email=email,
            customer_phone=phone,
            customer_kebele=kebele,
            customer_city=city,
            note=note,
            total_price=total_price
        )

       
        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                product_price=float(item['price']),
                quantity=item['quantity']
            )

        
        request.session['cart'] = {}

       
        send_mail(
            'Order Confirmation',
            f'Thank you for your order, {fname}! Your order ID is {order.id}. When the product is finished we will mail you',
            'yourshop@example.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, 'A new Order has arrived.')
        return redirect('shop')
    context = {
        'total': total_price,
    }
    return render(request, 'checkout.html',context)
