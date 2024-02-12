from services import views

from django.urls import path

from .views import *

app_name = "services"

urlpatterns = [
    path('view-services/',ServiceView.as_view(), name='view-services'),
    path('services/book/<int:service_id>/', BookServiceView.as_view(), name='book_service'),
]
 