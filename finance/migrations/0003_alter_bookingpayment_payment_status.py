# Generated by Django 4.1.2 on 2024-02-19 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_orderpayment_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingpayment',
            name='payment_status',
            field=models.CharField(choices=[('PN', 'Pending'), ('AP', 'Approved'), ('RJ', 'Rejected'), ('CP', 'Completed')], default='Pending', max_length=50),
        ),
    ]
