from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from accounts.decorators import required_access
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from accounts.models import User
from accounts.models import *
from accounts.forms import *


# Create your views here.
class LogoutView(View):

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, "You've logged out successfully.")
        return redirect('/')
    
    
class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "accounts/user-register.html"
    form_class = CustomerSignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:login')

    
def loginView(request):
    loginform = LoginForm(request.POST or None)
    msg = ''

    if request.method == 'POST':
        if loginform.is_valid():
            username = loginform.cleaned_data.get('username')
            password = loginform.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.user_type == "CM":
                login(request, user)
                return redirect('accounts:customer')
                
            elif user is not None and user.user_type == "DR":
                login(request, user)
                return redirect('accounts:driver')
            
            elif user is not None and user.user_type == "IM":
                login(request, user)
                return redirect('accounts:inventory_manager')
            
            elif user is not None and user.user_type == "SP":
                login(request, user)
                return redirect('accounts:service_provider')
            
            elif user is not None and user.user_type == "SR":
                login(request, user)
                return redirect('accounts:supplier')
            
            elif user is not None and user.user_type == "IS":
                login(request, user)
                return redirect('accounts:installer')
            
            elif user is not None and user.user_type == "FM":
                login(request, user)
                return redirect('accounts:finance_manager')
            else:
                messages.warning(request, 'Invalid Login credentials ')
                # msg = messages.error(request, 'Invalid form submission')
        else:
            messages.warning(request, 'Invalid form submission')
            msg = 'Invalid form submission'

    return render(request, 'accounts/user-login.html', {'form': loginform, 'msg': msg})


@required_access(login_url=reverse_lazy('accounts:login'), user_type="CM")
def customer(request):

    return redirect('store:view-products')


@required_access(login_url=reverse_lazy('accounts:login'), user_type="DR")
def driver(request):
    # orders = Order.objects.all()
    # # approved = orders.filter(orderstatus='Approved').count()
    # context = {
    #            #context
    # }

    return render(request, 'driver/pages/index.html')

@required_access(login_url=reverse_lazy('accounts:login'), user_type="IM")
def inventory_manager(request):
    # pending_cart_count = Order.objects.filter(payment__payment_status='Pending').count()
    # completed_cart_count = Order.objects.filter(payment__payment_status='Approved').count()
    # products = Product.objects.all()
    # total_products = products.count()
    # inStock = products.filter(in_stock=True)
    # total_inStock = inStock.count()
    # category  = Category.objects.all()
    # total_categories = category.count()
    # context = {
    #     'pending_cart_count': pending_cart_count,
    #     'completed_cart_count': completed_cart_count,
    #     'products':products,
    #     'total_products':total_products,
    #     'total_categories':total_categories,
    #     'total_inStock':total_inStock,
        
    # }

    return render(request, 'inventory_manager/pages/index.html')


@required_access(login_url=reverse_lazy('accounts:login'), user_type="IS")
def installer(request):
    # Fetch all poles that need to be installed
    # poles_to_install = Pole.objects.filter(installed=False) 


    return render(request, 'installer/pages/index.html')

@required_access(login_url=reverse_lazy('accounts:login'), user_type="SP")
def service_provider(request):
    # orders = Order.objects.all()
    # tasks = Task.objects.all()
    
   
    # context = {
    #           #content of the context

    # }

    return render(request, 'service_provider/pages/index.html')

@required_access(login_url=reverse_lazy('accounts:login'), user_type="FM")
def finance_manager(request):
    # orders = Order.objects.all()
    # total_orders = orders.count()
   
    
    # context = {'orders':orders,
    #           'total_orders':total_orders,
    # }

    return render(request, 'finance_manager/pages/index.html')

@required_access(login_url=reverse_lazy('accounts:login'), user_type="SR")
def supplier(request):
    user = request.user
    # all_tenders_count = SupplyTender.objects.count()
    # pending_tenders_count = SupplyTender.objects.filter(tender_status='Pending', user=user).count()
    # complete_tenders_count = SupplyTender.objects.filter(tender_status='Complete', user=user).count()
    # context = {
    #     'all_tenders_count': all_tenders_count,
    #     'pending_tenders_count': pending_tenders_count,
    #     'complete_tenders_count': complete_tenders_count,
    # }

    return render(request, 'supplier/pages/index.html')

#Change password
def password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/change-password.html', {'form': form})


