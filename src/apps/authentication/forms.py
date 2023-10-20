from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, PasswordChangeForm
from ckeditor.widgets import CKEditorWidget
from apps.authentication import enums, selectors, models

class RegisterUserForm(UserCreationForm):
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
    phone_number = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'custom-input',
        'placeholder': 'Phone Number'
    }))
    gender = forms.ChoiceField(choices=enums.GenderOptions.choices, widget=forms.RadioSelect(attrs={
        'class': 'custom-input-radio'
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
            'phone_number',
            'gender',
            'email',
            'password1', 
            'password2', 
            ]

class RegisterDoctorForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'First Name',
        'autofocus': 'true'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'LastName'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Email'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'custom-input',
        'placeholder': 'Phone Number'
    }))
    id_card = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'custom-input-file',
        'placeholder': 'Id Card'
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
            'phone_number',
            'id_card',
            'password1', 
            'password2', 
            ]

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Password'
    }))

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'LastName'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Email'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'custom-input',
        'placeholder': 'Phone Number'
    }))
    gender = forms.ChoiceField(choices=enums.GenderOptions.choices, widget=forms.RadioSelect(attrs={
        'class': 'custom-input-radio'
    }))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'custom-input',
        'type': 'date'
    }), required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 
            'last_name', 
            'email',
            'phone_number',
            'gender',
            'birth_date'
            ]
        
class UpdateDoctorUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'First Name'
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'LastName'
    }), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Email'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'custom-input',
        'placeholder': 'Phone Number'
    }))
    gender = forms.ChoiceField(choices=enums.GenderOptions.choices, widget=forms.RadioSelect(attrs={
        'class': 'custom-input-radio'
    }))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'custom-input',
        'type': 'date'
    }), required=False)
    currency_unit = forms.ChoiceField(choices=enums.CurrencyUnit.choices,  widget=forms.Select(attrs={
        'class': 'custom-input'
    }), required=False)
    about_doctor = forms.CharField(widget=CKEditorWidget(config_name="update_doctor"), required=False)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-input-file d-block',
        'placeholder': 'Avatar'
    }), required=False)
    country = forms.ModelChoiceField(queryset = selectors.country_list(), widget=forms.Select(attrs={
        'class': 'custom-input',
        'placeholder': 'Country',
        'id': 'id_country'
    }), required=False)
    city = forms.ModelChoiceField(queryset = selectors.city_list(), widget=forms.Select(attrs={
        'class': 'custom-input',
        'placeholder': 'City',
        'id': 'id_city'
    }), required=False)
    profession = forms.ModelChoiceField(queryset = selectors.profession_list(), widget=forms.Select(attrs={
        'class': 'custom-input',
        'placeholder': 'Profession'
    }), required=False)
    title = forms.ChoiceField(choices=enums.Title.choices, widget=forms.Select(attrs={
        'class': 'custom-input'
    }), required=False)
    orcid_account = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Orcid Account'
    }), required=False)
    pubmed_account = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Pubmed Account'
    }), required=False)
    diseases = forms.ModelMultipleChoiceField(queryset = selectors.disease_list(), widget=forms.CheckboxSelectMultiple(attrs={
        'class': 'custom-multi-choice-input',
        'placeholder': 'Disease',
        'name': 'disease'
    }), required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 
            'last_name', 
            'email',
            'phone_number',
            'gender',
            'birth_date',
            'currency_unit',
            'about_doctor',
            'avatar',
            'country',
            'city',
            'profession',
            'title',
            'orcid_account',
            'pubmed_account',
            'diseases'
        ]

    
class UpdatePatientUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'First Name'
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'LastName'
    }), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Email'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'custom-input',
        'placeholder': 'Phone Number'
    }))
    gender = forms.ChoiceField(choices=enums.GenderOptions.choices, widget=forms.RadioSelect(attrs={
        'class': 'custom-input-radio'
    }))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'custom-input',
        'type': 'date'
    }), required=False)
    
    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 
            'last_name', 
            'email',
            'phone_number',
            'birth_date',
            'gender'
        ]

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Password',
        "autocomplete": "current-password", 
        "autofocus": True
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'custom-input',
        'placeholder': 'New Password',
        "autocomplete": "new-password"
    }),
    strip=False,
    )
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Re-Type New Password',
        "autocomplete": "new-password"
    }), 
    strip=False
    )

class ExperienceForm(forms.ModelForm):
    experience_place = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Experience Place'
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Description'
    }), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'City'
    }))
    is_continue = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'id': 'is_continue_exp'
    }), required=False)
    start_year = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'custom-input',
        'id': 'start_year_exp'
    }))
    end_year = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'custom-input',
        'id': 'end_year_exp'
    }), required=False)

    class Meta:
        model = models.Experience
        fields = ('experience_place', 'description', 'city', 'is_continue', 'start_year', 'end_year')

class EducationForm(forms.ModelForm):
    education_place = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Education Place'
    }))
    education_branch = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Education Branch'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'City'
    }))
    is_continue = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'id': 'is_continue_edu'
    }), required=False)
    start_year = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'custom-input',
        'id': 'start_year_edu'
    }))
    end_year = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'custom-input',
        'id': 'end_year_edu'
    }), required=False)

    class Meta:
        model = models.Education
        fields = ('education_place', 'education_branch', 'city', 'is_continue', 'start_year', 'end_year')


class UserSocialMediaForm(forms.ModelForm):
    social_media_type = forms.ChoiceField(choices=enums.SocialMediaType.choices, widget=forms.Select(attrs={
        'class': 'custom-input'
    }), required=True)

    social_media_link = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'Social Media Url'
    }))


    class Meta:
        model = models.UserSocialMedia
        fields = ('social_media_type', 'social_media_link')

class PatientFileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-input',
        'placeholder': 'File name'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "rows":"5",
        "class": "custom-input d-block"
    }), required=False)
    patient_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'custom-input-file',
        'placeholder': 'File'
    }))

    class Meta:
        model = models.PatientsFile
        fields = ('name', 'description', 'patient_file')