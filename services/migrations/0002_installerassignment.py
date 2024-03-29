# Generated by Django 4.1.2 on 2024-03-13 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstallerAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('assigned', 'Assigned'), ('completed', 'Completed')], default='assigned', max_length=20)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='operator_assignment', to='services.servicebooking')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Assigned Service Booking',
                'verbose_name_plural': 'Assigned Service Bookings',
            },
        ),
    ]
