# Generated by Django 4.1.2 on 2024-03-12 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingpayment',
            name='address',
            field=models.IntegerField(null=True),
        ),
    ]