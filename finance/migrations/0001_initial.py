# Generated by Django 4.1.2 on 2024-05-21 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import finance.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("store", "0001_initial"),
        ("services", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_date", models.DateField(auto_now_add=True)),
                ("transaction_id", models.CharField(max_length=100, unique=True)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                            ("completed", "Completed"),
                        ],
                        default="Pending",
                        max_length=50,
                    ),
                ),
                ("county", models.CharField(max_length=100)),
                ("town", models.CharField(max_length=100)),
                (
                    "phone_number",
                    finance.models.CustomPhoneNumberField(
                        max_length=128, null=True, region=None
                    ),
                ),
                (
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="store.order"
                    ),
                ),
            ],
            options={
                "verbose_name": "Order Payment",
                "verbose_name_plural": "Order Payments",
            },
        ),
        migrations.CreateModel(
            name="BooKingPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=50)),
                ("address", models.IntegerField(null=True)),
                ("transaction_id", models.CharField(max_length=100, unique=True)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                            ("completed", "Completed"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
                ("payment_date", models.DateField(auto_now_add=True)),
                (
                    "booking",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="services.servicebooking",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Booking Payment",
                "verbose_name_plural": "Booking Payments",
            },
        ),
    ]
