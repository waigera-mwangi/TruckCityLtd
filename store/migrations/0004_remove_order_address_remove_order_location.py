# Generated by Django 4.1.2 on 2023-11-05 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_customer_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='location',
        ),
    ]
