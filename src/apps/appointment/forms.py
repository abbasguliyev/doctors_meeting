from django import forms
from apps.appointment.models import Availability, AppointmentRequest, DoctorNote
from apps.authentication import selectors, enums
from ckeditor.widgets import CKEditorWidget

class AvailabilityForm(forms.ModelForm):
    available_start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'type':'datetime',
        'class': 'custom-input'
    }))
    available_end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'type':'datetime',
        'class': 'custom-input'
    }))
    class Meta:
        model = Availability
        fields = ('available_start_time', 'available_end_time')

class AppointmentRequestCreateForm(forms.ModelForm):
    explanation = forms.CharField(widget=forms.TextInput(attrs={  
        'class': 'custom-input',
        'placeholder': 'Explanation'
    }))

    patient_file = forms.ModelChoiceField(queryset = None, widget=forms.Select(attrs={
        'class': 'custom-input',
        'placeholder': 'Patient File'
    }), required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            user = request.user
            patient = selectors.patient_profile_list().filter(user=user).last()
            self.fields['patient_file'].queryset = selectors.patient_file_list().filter(patient=patient)

    class Meta:
        model = AppointmentRequest
        fields = ('explanation',)

class AppointmentRequestUpdateForm(forms.ModelForm):
    doctor_request = forms.ChoiceField(choices=enums.DoctorAcceptedStatus.choices, widget=forms.Select(attrs={
        'class': 'custom-input'
    }))

    class Meta:
        model = AppointmentRequest
        fields = ('doctor_request',)

class DoctorNoteForm(forms.ModelForm):
    note = forms.CharField(widget=CKEditorWidget(config_name="default"), required=False)

    class Meta:
        model = DoctorNote
        fields = ('note',)