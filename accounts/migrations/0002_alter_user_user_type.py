# Generated by Django 4.1.2 on 2023-09-22 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('CM', 'CUSTOMER'), ('DR', 'DRIVER'), ('IM', 'INVENTORY MANAGER'), ('SP', 'SERVICE PROVIDER'), ('SR', 'SUPPLIER'), ('IS', 'INSTALLER'), ('FM', 'FINANCE MANAGER'), ('AD', 'ADMIN')], default='CM', max_length=2),
        ),
    ]
