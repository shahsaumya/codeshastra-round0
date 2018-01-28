# Create your models here
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


def convert_to_dict(obj):
    return obj.__dict__


class Student_Detail(models.Model):
    name = models.CharField(max_length=20, blank=True)
    sap_id = models.BigIntegerField(validators=[MaxValueValidator(
        99999999999), MinValueValidator(10000000000)])

    address = models.CharField(max_length=50, blank=True)
    dob = models.CharField(max_length=10, validators=[
                           RegexValidator(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$')], blank=True)

    mobile_no = models.BigIntegerField(validators=[MaxValueValidator(
        9999999999), MinValueValidator(1000000000)])

    dept = models.CharField(max_length=20, blank=True)
    pic = models.FileField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return convert_to_dict(self)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    mobile_no = models.BigIntegerField(validators=[MaxValueValidator(
        9999999999), MinValueValidator(1000000000)])

    designation = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def to_dict(self):
        return convert_to_dict(self)
