from django.urls import path, reverse_lazy
from accounts import views
from accounts.views import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from accounts.decorators import required_access
from .views import *

app_name = "feedback"

urlpatterns = [

   # faqs
    path('customer-faq/', FAQQuestionTypeListView.as_view(), name='faq_question_types'),
    path('driver-faq/', D_FAQ.as_view(), name='driver-faq'),
    path('supplier-faq/', S_FAQ.as_view(), name='supplier-faq'),
    path('installerr-faq/', I_FAQ.as_view(), name='installer-faq'),
    path('inventory-faq/', IV_FAQ.as_view(), name='inventory-faq'),
    path('service-faq/', SP_FAQ.as_view(), name='service-faq'),
    path('finance-faq/', F_FAQ.as_view(), name='finance-faq'),
    path('about-us/', about_us, name='about-us'),
    
    
     #  feedback urls
    path('customer/view/feedback/', customer_feedback_view, name='customer_feedback'),
    path('finance/view/feedback/', finance_feedback_view, name='finance_feedback'),
    path('inventory/view/feedback/', inventory_feedback_view, name='inventory_feedback'),
    path('brander/view/feedback/', installer_feedback_view, name='installer_feedback'),
    path('supplier/view/feedback/', supplier_feedback_view, name='supplier_feedback'),
    path('dispatch/view/feedback/', service_feedback_view, name='service_feedback'),
    path('driver/view/feedback/', driver_feedback_view, name='driver_feedback'),
    
    # send feedback urls
    path('feedback/customer/send/', customer_send_feedback_view, name='customer_send_feedback'),
    path('feedback/finance/send/', finance_send_feedback_view, name='finance_send_feedback'),
    path('feedback/inventory/send/', inventory_send_feedback_view, name='inventory_send_feedback'),
    path('feedback/installer/send/', installer_send_feedback_view, name='installer_send_feedback'),
    path('feedback/supplier/send/', supplier_send_feedback_view, name='supplier_send_feedback'),
    path('feedback/service/send/', service_send_feedback_view, name='service_send_feedback'),
    path('feedback/driver/send/', driver_send_feedback_view, name='driver_send_feedback'),

]