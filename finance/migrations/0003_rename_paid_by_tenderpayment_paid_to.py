# Generated by Django 4.1.2 on 2024-06-02 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_tenderpayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenderpayment',
            old_name='paid_by',
            new_name='paid_to',
        ),
    ]
