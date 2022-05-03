from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.modelfields import PhoneNumberField

class NewStudentForm(UserCreationForm):
    GENDER = [
        ('M',  'Male') , 
        ('F',  'Female')
    ]
    FACULTY = [
        ('EDU', 'Education'),
        ('ENG', 'Engineering and Natural Sciences'),
        ('BS', 'Business School'),
        ('L', 'Law')
    ]
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    course = forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER)
    faculty = forms.ChoiceField(choices=FACULTY)

    class Meta:
        model = User
        fields = ("first_name","last_name","username",  "email","course", "gender","faculty", "password1", "password2")
        
class NewTeacherForm(UserCreationForm):
    GENDER = [
        ('M',  'Male') , 
        ('F',  'Female')
    ]
    fname = forms.CharField(max_length=200)
    lname = forms.CharField(max_length=200)
    email = forms.EmailField()
    phoneNumber = PhoneNumberField(null = False, blank = False).formfield()
    gender = forms.ChoiceField(choices=GENDER)

    class Meta:
        model = User
        fields = ("fname","lname","username",  "email", "phoneNumber", "gender", "password1", "password2")