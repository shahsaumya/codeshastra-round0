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
        99999999999), MinValueValidator(10000000000)], primary_key=True)

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

    sap_id = models.BigIntegerField(validators=[MaxValueValidator(
        99999999999), MinValueValidator(10000000000)], primary_key=True)

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


class Student_Allotment(models.Model):
    student = models.ForeignKey(Student_Detail, on_delete=models.CASCADE)

    room_name = models.CharField(max_length=40)
    date = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    exam = models.CharField(max_length=300)

    def __str__(self):
        return self.student.name

    def to_dict(self):
        return convert_to_dict(self)


class Teacher_Allotment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=40)
    date = models.CharField(max_length=40)
    time = models.CharField(max_length=40)

    def __str__(self):
        return self.teacher.user.username

    def to_dict(self):
        return convert_to_dict(self)


class Room(models.Model):
    room_no = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=40)
    capacity = models.IntegerField()
    floor = models.CharField(max_length=10)

    def __str__(self):
        return self.room_name

    def to_dict(self):
        return convert_to_dict(self)
