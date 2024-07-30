from django.shortcuts import render
from django.views.generic import CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
# faq
class FAQQuestionTypeListView(ListView):
    template_name = 'faq/customer_faq.html'
    queryset = FAQ.objects.filter(question_types='CM')
    context_object_name = 'faqs'

class D_FAQ(ListView):
    template_name = 'faq/driver_faq.html'
    queryset = FAQ.objects.filter(question_types='DR')
    context_object_name = 'faqs'

class S_FAQ(ListView):
    template_name = 'faq/supplier_faq.html'
    queryset = FAQ.objects.filter(question_types='SR')
    context_object_name = 'faqs'

class I_FAQ(ListView):
    template_name = 'faq/installer_faq.html'
    queryset = FAQ.objects.filter(question_types='IS')
    context_object_name = 'faqs'

class IV_FAQ(ListView):
    template_name = 'faq/inventory_faq.html'
    queryset = FAQ.objects.filter(question_types='IM')
    context_object_name = 'faqs'

class SP_FAQ(ListView):
    template_name = 'faq/service_faq.html'
    queryset = FAQ.objects.filter(question_types='SP')
    context_object_name = 'faqs'

class F_FAQ(ListView):
    template_name = 'faq/finance_faq.html'
    queryset = FAQ.objects.filter(question_types='FM')
    context_object_name = 'faqs'

def about_us(request):
    return render(request, 'includes/about-us.html')



# customer feedback view
def customer_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/customer_feedback.html', {'conversations': conversations,})

# finance feedback views
def finance_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/finance_feedback.html', {'conversations': conversations,})

# inventory feedback views
def inventory_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/inventory_feedback.html', {'conversations': conversations,})

# installer feedback views
def installer_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/installer_feedback.html', {'conversations': conversations,})

# service feedback views
def service_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/service_feedback.html', {'conversations': conversations,})

# supplier feedback views
def supplier_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/supplier_feedback.html', {'conversations': conversations,})

#driver customer feedback views
def driver_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/driver_feedback.html', {'conversations': conversations,})

# customer feedback submission
def customer_send_feedback_view(request):
    if request.method == 'POST':
        form = CustomerFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('feedback:customer_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = CustomerFeedbackForm()
    
    return render(request, 'feedback/send_feedback/customer_send_feedback.html', {'form': form})

# finance feedback submission
def finance_send_feedback_view(request):
    if request.method == 'POST':
        form = FinanceFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('feedback:finance_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = FinanceFeedbackForm()
    
    return render(request, 'feedback/send_feedback/finance_send_feedback.html', {'form': form})

# inventory feedback submission
def inventory_send_feedback_view(request):
    if request.method == 'POST':
        form = InventoryFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('feedback:inventory_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = InventoryFeedbackForm()
    
    return render(request, 'feedback/send_feedback/inventory_send_feedback.html', {'form': form})

# installer feedback submission
def installer_send_feedback_view(request):
    if request.method == 'POST':
        form = InstallerFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('feedback:installer_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = InstallerFeedbackForm()
    
    
    return render(request, 'feedback/send_feedback/installer_send_feedback.html', {'form': form})

# supplier feedback submission
def supplier_send_feedback_view(request):
    if request.method == 'POST':
        form = SupplierFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('feedback:supplier_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = SupplierFeedbackForm()
    
    return render(request, 'feedback/send_feedback/supplier_send_feedback.html', {'form': form})

# service feedback submission
def service_send_feedback_view(request):
    if request.method == 'POST':
        form = ServiceFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('feedback:service_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = ServiceFeedbackForm()
    
    return render(request, 'feedback/send_feedback/service_send_feedback.html', {'form': form})

# driver feedback submission
def driver_send_feedback_view(request):
    if request.method == 'POST':
        form = DriverFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('feedback:driver_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = DriverFeedbackForm()
    
    return render(request, 'feedback/send_feedback/driver_send_feedback.html', {'form': form})

def about_us(request):
    return render(request, 'customer/pages/about-us.html')

# contact us
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback:contact_success')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'feedback/send_feedback/contact_us.html', {'form': form})


def contact_success(request):
    return render(request, 'feedback/send_feedback/contact_success.html')
