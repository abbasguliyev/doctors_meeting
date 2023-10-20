from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from apps.authentication import enums, selectors, models
from apps.pages.models import Contact, AdsComment, Ads

class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email'
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'form-control',
        'placeholder': 'Enter Subject'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'form-control',
        'placeholder': 'Enter Phone'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={  
        "rows":"5",
        "class": "form-control d-block",
        'placeholder': 'Enter Message'
    }))

    class Meta:
        model = Contact
        fields = [
            'name', 
            'email',
            'subject', 
            'phone', 
            'message'
        ]

class AdsCommentForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=selectors.user_list(), required=False)
    ads = forms.ModelChoiceField(queryset=Ads.objects.all(), required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={  
        "rows":"5",
        "class": "form-control d-block",
        'placeholder': 'Enter Comment'
    }))

    class Meta:
        model = AdsComment
        fields = ['owner', 'ads', 'comment']
    

class DashboardRegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'First Name',
        'autofocus': 'true'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'custom-input',
        'placeholder': 'LastName'
    }))
    user_type = forms.ChoiceField(choices=enums.UserType.choices,  widget=forms.Select(attrs={
        'class': 'custom-input'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Re-Type Password'
    }))

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 
            'last_name', 
            'email',
            'user_type',
            'password1', 
            'password2', 
            ]
