from app.models import Teacher, Student_Detail
from django.contrib.auth.models import User
from django import forms


class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "input-lg", 'size': "40"})
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        labels = {
            'first_name': ('First Name'),
            'last_name': ('Last Name'),
            'username': ('Username'),
            'password': ('Password'),
        }


class TeacherProfileForm(forms.ModelForm):
    sap_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    mobile_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    designation = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    class Meta:
        model = Teacher
        fields = ('sap_id', 'mobile_no', 'designation',)
        labels = {
            'sap_id': ('SAP-ID'),
            'mobile_no': ('Mobile Number'),
            'designation': ('Designation'),
        }


class Student_DetailForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    sap_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    dob = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    mobile_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input-lg", 'size': "40"}),
    )

    class Meta:
        model = Student_Detail
        fields = ('name', 'sap_id', 'address',
                  'dob', 'mobile_no', 'dept', 'pic',)
        labels = {
            'name': ('Name'),
            'sap_id': ('SAP-ID'),
            'address': ('Address'),
            'dob': ('Date of Birth'),
            'mobile_no': ('Mobile No'),
            'dept': ('Department'),
            'pic': ('Photo'),
        }
