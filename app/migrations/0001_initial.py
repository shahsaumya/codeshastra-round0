# Generated by Django 2.0.1 on 2018-01-28 04:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('sap_id', models.BigIntegerField(validators=[django.core.validators.MaxValueValidator(99999999999), django.core.validators.MinValueValidator(10000000000)])),
                ('address', models.CharField(blank=True, max_length=50)),
                ('dob', models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]{2}/[0-9]{2}/[0-9]{4}$')])),
                ('mobile_no', models.BigIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1000000000)])),
                ('dept', models.CharField(blank=True, max_length=20)),
                ('pic', models.FileField(blank=True, upload_to='')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_no', models.BigIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1000000000)])),
                ('designation', models.CharField(blank=True, max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
