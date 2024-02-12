from django import forms
from django.forms import ModelForm
from .models import *

from store.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'