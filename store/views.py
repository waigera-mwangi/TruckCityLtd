from django.views import View
from django.forms import inlineformset_factory
from django.db.models import Sum, F
from finance.utils import calculate_delivery_fee
from django.contrib.auth.decorators import login_required 
from djmoney.money import Money

from django.http import HttpResponse
from accounts.models import User
from io import BytesIO
# from utils.utils import generate_key
from xhtml2pdf import pisa
from django.http import JsonResponse
from store.models import * 
from django.views import View
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import *
from .models import Product
from finance.models import *
from shipping.models import *
from django.db.models import Q


# custoomer viewing products
class ProductView(View):
    def get(self, request):
        products =  Product.objects.all()
        context = {'products': products}
        return render(request, 'customer/pages/index.html', context)

# cart functions

# @login_required
def add_to_cart(request, pk):
    quantity = request.GET.get('quantity', 1)
    product = get_object_or_404(Product, pk=pk)

    # Check if requested quantity is in stock
    if product.quantity < int(quantity):
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('store:view-products')

    # Check if the total quantity in the order exceeds the available stock
    order_items = OrderItem.objects.filter(product=product, order__is_completed=False, order__user=request.user)
    total_quantity_in_order = sum(order_item.quantity for order_item in order_items)
    if product.quantity < total_quantity_in_order + int(quantity):
        messages.error(request, f"Only {product.quantity } {product.name} available in stock.")
        return redirect('store:view-products')

    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += int(quantity)
    order_item.save()
    messages.success(request, 'Item added to cart.', extra_tags='text-success')
    return redirect('store:view-products')

# @login_required
def view_cart(request):
    user = User.objects.all()
    
    # Retrieve the latest pending order if one exists, otherwise create a new one
    try:
        order = Order.objects.filter(user=request.user, is_completed=False).latest('id')
    except Order.DoesNotExist:
        order = Order.objects.create(user=request.user)

    order_items = order.orderitem_set.all()

    if request.method == 'POST':
        if 'order_item_id' in request.POST:
            # Handle updates to order items
            order_item_id = int(request.POST.get('order_item_id'))
            order_item = OrderItem.objects.get(id=order_item_id, order=order)

            if 'increment' in request.POST:
                order_item.quantity += 1
                order_item.save()
                messages.success(request, 'Quantity updated successfully.', extra_tags='text-success')

            if 'decrement' in request.POST:
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.success(request, 'Quantity updated successfully.', extra_tags='text-success')
                else:
                    order_item.delete()
                    messages.success(request, 'Item removed from order.', extra_tags='text-success')

                    
    # Calculate the subtotal for each order item and save it
    for item in order_items:
        item.subtotal = item.product.price * item.quantity
        item.save()

    # Calculate the order total by summing the subtotals of each order item
    order_total = sum([item.subtotal for item in order_items])

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'customer/pages/cart.html', context)


def customer_order_list(request):
        user = request.user
        orders = Order.objects.filter(user=user, is_completed=True)
        order_list = []
        for order in orders:
            payment = OrderPayment.objects.filter(order=order).first()
            if payment:
                order_info = {
                    'transaction_id': payment.transaction_id,
                    'username': order.user.username,
                    'quantity': order.pole.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                    # 'total_cost': order.subtotal,
                    'payment_status': payment.payment_status,
                    'order_date': order.order_date,
                    'order_id': order.id,  # Add cart_id to the dictionary
                }
                order_list.append(order_info)
        return render(request, 'customer/pages/customer_order_list.html', {'order_list': order_list})    


def customer_order_detail(request, order_id):
    user = request.user
    order = get_object_or_404(Order, user=user, id=order_id, is_completed=True)
    payment = OrderPayment.objects.filter(order=order).first()
    order_items = order.orderitem_set.all()

    # Calculate the order total
    order_total = order.orderitem_set.annotate(
        item_total=F('quantity') * F('product__price')
    ).aggregate(total_cost=Sum('item_total'))['total_cost']

    # Ensure order_total is a Money object
    order_total_money = Money(Decimal(order_total), 'KES')

    # Calculate the delivery fee
    delivery_fee = calculate_delivery_fee(order_total_money)

    # Add the delivery fee to the order total
    total_with_delivery = order_total_money + delivery_fee

    context = {
        'order': order,
        'payment': payment,
        'order_items': order_items,
        'order_total': total_with_delivery,
    }
    return render(request, 'customer/pages/customer_order_detail.html', context)

def customer_order_invoice(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_completed=True)
    order_list = []
    for order in orders:
        payment = OrderPayment.objects.filter(order=order).first()
        if payment:
            # Calculate the order total
            order_total = order.orderitem_set.annotate(
                item_total=F('quantity') * F('product__price')
            ).aggregate(total_cost=Sum('item_total'))['total_cost']

            # Ensure order_total is a Money object
            order_total_money = Money(Decimal(order_total), 'KES')

            # Calculate the delivery fee
            delivery_fee = calculate_delivery_fee(order_total_money)

            # Add the delivery fee to the order total
            total_with_delivery = order_total_money + delivery_fee

            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'quantity': order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum'],
                'order_total': total_with_delivery,  # Use the total with delivery
                'payment_status': payment.payment_status,
                'order_date': order.order_date,
                'order_id': order.id,  # Add order_id to the dictionary
            }
            order_list.append(order_info)
    return render(request, 'customer/pages/customer-invoice.html', {'order_list': order_list})



def customer_order_pdf(request, order_id):
    user = request.user
    order = get_object_or_404(Order, user=user, id=order_id, is_completed=True)
    payment = OrderPayment.objects.filter(order=order).first()
    order_items = order.orderitem_set.all()
    order_date = order.order_date

    # Calculate order total as Money object
    order_total = Money(
        order.orderitem_set.annotate(
            item_total=F('quantity') * F('product__price')
        ).aggregate(
            total_cost=Sum('item_total')
        )['total_cost'] or 0, 'KES'
    )

    # Calculate delivery fee
    delivery_fee = calculate_delivery_fee(order_total)
    total_with_delivery = order_total + delivery_fee

    # Load template for receipt
    template = get_template('customer/pages/order_payment_receipt.html')
    context = {
        'order': order,
        'order_date': order_date,
        'payment': payment,
        'order_items': order_items,
        'order_total': order_total,
        'delivery_fee': delivery_fee,
        'total_with_delivery': total_with_delivery,
        'user': user,
    }
    html = template.render(context)

    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), buffer)

    if not pdf.err:
        # Get the value of the BytesIO buffer and write it to the response
        pdf_value = buffer.getvalue()
        buffer.close()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="order_invoice_{}.pdf"'.format(order_id)
        response.write(pdf_value)
        return response

    return HttpResponse('Error generating PDF!')
@login_required
def pending_orders(request):
    orders = Order.objects.filter(is_completed=True)
    order_list = []
    for order in orders:
        order_payment = OrderPayment.objects.filter(order=order, payment_status='pending').first()
        if order_payment:
            quantity = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
            
            # Annotate order items to include product price and calculate item total
            order_total = order.orderitem_set.annotate(
                item_total=F('quantity') * F('product__price')
            ).aggregate(
                total_cost=Sum('item_total')
            )['total_cost']
            
            # Ensure order_total is a Money object
            order_total = Money(Decimal(order_total), 'KES')
            delivery_fee = calculate_delivery_fee(order_total)
            total_with_delivery = order_total + delivery_fee

            order_info = {
                'transaction_id': order_payment.transaction_id,
                'username': order.user.username,
                'quantity': quantity,
                'order_total': total_with_delivery,
                'payment_status': order_payment.payment_status,
                'date_ordered': order.order_date,
                'payment_id': order_payment.id,
            }
            order_list.append(order_info)
    return render(request, 'finance_manager/pages/pending-orders.html', {'order_list': order_list})

def approved_orders(request):
    orders = Order.objects.filter(is_completed=True)
    order_list = []
    for order in orders:
        order_payment = OrderPayment.objects.filter(order=order, payment_status='approved').first()
        if order_payment:
            quantity = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
            
            # Annotate order items to include product price and calculate item total
            order_total = order.orderitem_set.annotate(
                item_total=F('quantity') * F('product__price')
            ).aggregate(
                total_cost=Sum('item_total')
            )['total_cost']
            
            # Ensure order_total is a Money object
            order_total = Money(Decimal(order_total), 'KES')
            delivery_fee = calculate_delivery_fee(order_total)
            total_with_delivery = order_total + delivery_fee

            order_info = {
                'transaction_id': order_payment.transaction_id,
                'username': order.user.username,
                'quantity': quantity,
                'order_total': total_with_delivery,
                'payment_status': order_payment.payment_status,
                'date_ordered': order.order_date,
                'payment_id': order_payment.id,
            }
            order_list.append(order_info)
    return render(request, 'finance_manager/pages/approved-orders.html', {'order_list': order_list})

def order_rejected_payment(request):
    orders = Order.objects.filter(is_completed=True)
    order_list = []
    for order in orders:
        order_payment = OrderPayment.objects.filter(order=order, payment_status='rejected').first()
        if order_payment:
            quantity = order.orderitem_set.aggregate(Sum('quantity'))['quantity__sum']
            
            # Annotate order items to include product price and calculate item total
            order_total = order.orderitem_set.annotate(
                item_total=F('quantity') * F('product__price')
            ).aggregate(
                total_cost=Sum('item_total')
            )['total_cost']
            
            # Ensure order_total is a Money object
            order_total = Money(Decimal(order_total), 'KES')
            delivery_fee = calculate_delivery_fee(order_total)
            total_with_delivery = order_total + delivery_fee

            order_info = {
                'transaction_id': order_payment.transaction_id,
                'username': order.user.username,
                'quantity': quantity,
                'order_total': total_with_delivery,
                'payment_status': order_payment.payment_status,
                'date_ordered': order.order_date,
                'payment_id': order_payment.id,
            }
            order_list.append(order_info)
    return render(request, 'finance_manager/pages/rejected-orders.html', {'order_list': order_list})


def approve_payments(request, transaction_id):
    payment = get_object_or_404(OrderPayment, transaction_id=transaction_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'approved':
            payment.payment_status = 'approved'
            # Additional logic if needed
        elif status == 'rejected':
            payment.payment_status = 'rejected'
            # Additional logic if needed
        
        payment.save()  # Save the payment status change
        return redirect('store:pending_orders')  # Redirect to the pending payment list view after processing
    
    # If the request method is GET, render the template with the payment details
    context = {'payment': payment}
    return render(request, 'finance_manager/pages/pending-orders.html', context)



User = get_user_model()

def assign_driver_order_list(request):
    orders = Order.objects.filter(is_completed=True, shipping__isnull=True)
    order_list = []
    for order in orders:
        payment = OrderPayment.objects.filter(order=order, payment_status='approved').first()
        if payment:
            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'payment_status': payment.payment_status,
                'county': payment.county,
                'town': payment.town,
                'phone_number': payment.phone_number,
                'date_ordered': order.order_date,
                'payment_id': payment.id,
                'id': order.id,
                'driver': None,
               
            }
            shipping = Shipping.objects.filter(order=order).first()
            if shipping:
                order_info['driver'] = shipping.driver
            order_list.append(order_info)

    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        driver_id = request.POST.get('driver_id', None)
        if order_id and driver_id:
            try:
                order = Order.objects.get(pk=order_id)
                if Shipping.objects.filter(order=order).exists():
                    messages.error(request, f"Order has already been assigned to a driver")
                else:
                    driver = User.objects.filter(pk=driver_id, user_type=User.UserTypes.DRIVER).first()
                    shipping = Shipping.objects.create(order=order, driver=driver)
                    messages.success(request, f"Order has been assigned to {driver}")
            except (Order.DoesNotExist, User.DoesNotExist):
                messages.error(request, "Failed to assign driver.")
        else:
            messages.error(request, "Missing Order Id or Driver Id")

        return redirect('store:assign-order-list')


    drivers = User.objects.filter(user_type=User.UserTypes.DRIVER)
    return render(request, 'service_provider/pages/assign_order_list.html', {'order_list': order_list, 'drivers': drivers})



def assigned_order_list(request):
    # Filter orders with is_completed=True and associated shipping with a status other than "Delivered" or "Complete"
    orders = Order.objects.filter(
        is_completed=True,
        shipping__isnull=False
    ).exclude(
        shipping__status=Shipping.Status.DELIVERED
    ).exclude(
        shipping__status=Shipping.Status.COMPLETE
    )
    
    order_list = []
    for order in orders:
        payment = OrderPayment.objects.filter(order=order, payment_status='approved').first()
        if payment:
            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'quantity': order.pole.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                'order_total' : order.pole.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost'],
                'payment_status': payment.payment_status,
                'county':payment.county,
                'town':payment.town,
                'phone_number':order.user.phone_number,
                'date_ordered': order.order_date,
                'payment_id': payment.id,
                'id': order.id,
                'driver': None,
               
            }
            shipping = Shipping.objects.filter(order=order).first()
            if shipping:
                order_info['driver'] = shipping.driver
            order_list.append(order_info)

    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        driver_id = request.POST.get('driver_id', None)
        if order_id and driver_id:
            try:
                order = Order.objects.get(pk=order_id)
                if Shipping.objects.filter(order=order).exists():
                    messages.error(request, f"{order} has already  assigned to a driver")
                else:
                    driver = User.objects.filter(pk=driver_id, user_type=User.UserTypes.DRIVER).first()
                    shipping = Shipping.objects.create(order=order, driver=driver)
                    messages.success(request, f"{order} has been assigned to {driver}")
            except (Order.DoesNotExist, User.DoesNotExist):
                messages.error(request, "Failed to assign driver.")
        else:
            messages.error(request, "Missing Order Id or Driver Id.")

        return redirect('inventory:assigned-order-list')


    drivers = User.objects.filter(user_type=User.UserTypes.DRIVER)
    return render(request, 'service_provider/pages/assigned_order_list.html', {'order_list': order_list, 'drivers': drivers})

# inventory
class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory_manager/pages/product_detail.html'
    context_object_name = 'product'


class ProductDetailViewCustomer(DetailView):
    model = Product
    template_name = 'inventory_manager/pages/product_detail_customer.html'
    context_object_name = 'product'
    
class ProductListView(ListView):
    model = Product
    template_name = 'inventory_manager/pages/product_list.html'
    context_object_name = 'products'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory_manager/pages/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('store:product-list')

    def form_valid(self, form):
        # Set the user of the product to the currently logged in user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add error messages to the form if it is invalid
        messages.error(self.request, 'An error occurred. Please try again.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        # Set the user of the product to the currently logged in user
        request.POST = request.POST.copy()
        request.POST['user'] = request.user.id
        return super().post(request, *args, **kwargs)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'inventory_manager/pages/product_update_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('store:product-list')

    def test_func(self):
        return self.request.user.is_superuser

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory_manager/pages/product_confirm_delete.html'
    success_url = reverse_lazy('store:product-list')

    def test_func(self):
        return self.request.user.is_superuser

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'


def create_category(request):
    form  = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully")
            return redirect('store:inventory_category_list')
        else:
            messages.warning(request, "Error creating Category")
    context = {'form': form}
    return render(request, 'inventory_manager/pages/add-category.html', context)

def inventory_category_list(request):
    category = Category.objects.filter()
    context = {"category":category}
    return render(request, "inventory_manager/pages/category-list.html", context)

# update category
def update_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully")
            return redirect('store:inventory_category_list')
        else:
            messages.warning(request, "Error updating Category")
    context = {'form': form}
    return render(request, 'inventory_manager/pages/add-category.html', context)

