# Generated by Django 4.1.2 on 2024-03-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='question_types',
            field=models.CharField(choices=[('DR', 'Driver'), ('FM', 'Finance Manager'), ('IM', 'Inventory Manager'), ('SR', 'Supplier'), ('CM', 'Customer'), ('IS', 'Installer'), ('SP', 'Service Provider')], default='CM', max_length=3, verbose_name='question Type'),
        ),
    ]
