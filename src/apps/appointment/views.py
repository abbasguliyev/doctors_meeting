from datetime import datetime, timedelta
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.core import serializers
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from apps.appointment import selectors, tasks, enums
from apps.authentication import selectors as auth_selectors, enums as auth_enums
from apps.appointment.forms import (
    AvailabilityForm,
    AppointmentRequestCreateForm,
    AppointmentRequestUpdateForm,
    DoctorNoteForm
)
from apps.appointment.models import Availability, AppointmentRequest, AppointmentRequestFile, RoomMember, Meeting, DoctorNote

import os
from doctors_meeting import settings
from django.http import JsonResponse, HttpResponse, Http404

import random
import time
from agora_token_builder import RtcTokenBuilder
import json
from django.views.decorators.csrf import csrf_exempt

class AvailabilityView(LoginRequiredMixin, TemplateView):
    template_name = 'availability.html'
    redirect_authenticated_user = True

class AvailabilitySearchView(View):
    template_name = "availability_search.html"

    def get(self, request, *args, **kwargs):
        context = {}
        date_str = self.request.GET.get('date')
        available_user_id = kwargs.get('available_user_id')
        print(f'{available_user_id=}')
        if date_str is not None:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date:
                user = auth_selectors.user_list().filter(pk=available_user_id).last()
                availabilities = selectors.availability_list().filter(available_user=user, available_start_time__year=date.year, available_start_time__month = date.month, available_start_time__day = date.day)
            context["availabilities"] = availabilities
        return render(request, self.template_name, context)

class AvailabilityCreateView(LoginRequiredMixin, View):
    template_name = "availability_create.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        now = timezone.now().date()
        date_str = self.request.POST.get("date")
        start_time = self.request.POST.get("start_time")
        end_time = self.request.POST.get("end_time")
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        if date < now:
            messages.error(request, "You cannot be available in the past!")
            return redirect("availability")
        
        if int(end_time) <= int(start_time):
            messages.error(request, "End Time cannot less or equal than Start Time!")
            return redirect("availability")
        
        for i in range(int(start_time), int(end_time)):
            start_time_str = f"{date.year}-{date.month}-{date.day} {i}:00:00"
            start_time_date = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            end_time_date = start_time_date + timedelta(hours=1)
            availability = selectors.availability_list().filter(
                available_user=request.user, 
                available_start_time = start_time_date, 
                available_end_time = end_time_date
            ).last()
            if availability is not None:
                continue
            
            new_availability = Availability.objects.create(
                available_start_time = start_time_date, 
                available_end_time = end_time_date,
                reserved = False,
                available_user = request.user
            )
            new_availability.full_clean()
            new_availability.save()
        
        messages.success(request, "Availability Time successfully added")
        return redirect("availability")
    
class AvailabilityDeleteView(LoginRequiredMixin, DeleteView):
    model = Availability
    success_url = reverse_lazy('availability')
    template_name = "availability_delete.html"

class AppointmentRequestView(LoginRequiredMixin, ListView):
    model = AppointmentRequest
    template_name = "appointment_request.html"
    context_object_name = "appointment_requests"

    def get_queryset(self):
        if self.request.user.is_superuser == True or  self.request.user.user_type == auth_enums.UserType.health_representative:
            queryset = super().get_queryset().all()
        else:
            queryset = super().get_queryset().filter(Q(doctor=self.request.user) | Q(owner=self.request.user))
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        current_date = timezone.now()
        context['appointment_requests'] = self.get_queryset().order_by('-appointment_date', 'doctor_request')[:10]
        context['current_date'] = current_date
        return context
    

class AppointmentRequestSearchView(View):
    template_name = "appointment_request_search.html"

    def get_queryset(self):
        queryset = selectors.appointment_request_list().filter(Q(doctor=self.request.user) | Q(owner=self.request.user))
        return queryset

    def get(self, request, *args, **kwargs):
        context = {}
        date_str = self.request.GET.get('date')
        current_date = timezone.now()

        if date_str is not None:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date:
                appointment_requests = self.get_queryset().filter(appointment_date__year=date.year, appointment_date__month = date.month, appointment_date__day = date.day)
            context["appointment_requests"] = appointment_requests
            context['current_date'] = current_date
        return render(request, self.template_name, context)


class AppointmentRequestCreateView(LoginRequiredMixin, View):
    def get(self, request, availability_id):
        form = AppointmentRequestCreateForm(request=request)
        # patient_files = auth_selectors.patient_file_list().filter(patient=request.user)
        return render(request, 'appointment_request_create.html', {'form': form})
    
    def post(self, request, availability_id):
        form = AppointmentRequestCreateForm(request.POST, request=request)
        if form.is_valid():
            appointment_date = form.cleaned_data.get("appointment_date")
            owner_apt_req = selectors.appointment_request_list().filter(appointment_date=appointment_date).count()
            if owner_apt_req > 0:
                messages.error(self.request, "You cannot request more than 1 appointment in same date!")
                return redirect('doctors')
            appointment_request = form.save(commit=False)
            patient_file = form.cleaned_data.pop('patient_file')
            appointment_request.owner = self.request.user
            availability_obj = selectors.availability_list().filter(pk=availability_id).last()
            appointment_request.doctor = availability_obj.available_user
            appointment_request.availability = availability_obj
            appointment_request.appointment_date = availability_obj.available_start_time
            appointment_request.save()
            if patient_file is not None:
                appointment_request_file = AppointmentRequestFile.objects.create(appointment_request=appointment_request, patient_file=patient_file)
                appointment_request_file.save()
            transaction.on_commit(lambda: tasks.send_appointment_request_mail_task.delay(appointment_request.doctor.id, "Appointment request sended"))
            transaction.on_commit(lambda: tasks.send_appointment_request_mail_task.delay(self.request.user.id, "Appointment request sended"))
            messages.success(self.request, "Appointment request successfully sended!")
        return redirect('index')
    
class AppointmentRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = AppointmentRequest
    form_class = AppointmentRequestUpdateForm
    template_name = 'appointment_request_update.html'
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['patient_files'] = selectors.appointment_request_file_list().filter(appointment_request=self.get_object())
        return context
    
    def form_valid(self, form):
        appointment_request = form.save(commit=False)

        if self.request.POST.get('patient_file') == 'true':
            appointment_request_file = selectors.appointment_request_file_list().filter(appointment_request=self.get_object()).last()
            appointment_request_file.is_downloaded = True
            appointment_request_file.save()
        
        if form.cleaned_data.get('doctor_request') == "Accepted":
            availability = appointment_request.availability
            availability.reserved = True
            availability.save()
            transaction.on_commit(lambda: tasks.send_appointment_request_accepted_mail_task.delay(appointment_request.owner.id, appointment_request.id))
        appointment_request.save()
        messages.success(self.request, "Appointment request updated")
        return super().form_valid(form)
    
class NoteView(LoginRequiredMixin, ListView):
    model = DoctorNote
    template_name = "notes.html"
    context_object_name = "notes"

    def get_queryset(self) -> QuerySet[Any]:
        qs = DoctorNote.objects.select_related('doctor', 'meeting').filter(doctor=self.request.user)
        return qs
    
class NoteDetailView(LoginRequiredMixin, UpdateView):
    model = DoctorNote
    form_class = DoctorNoteForm
    template_name = 'note_detail.html'
    success_url = reverse_lazy('notes')
    context_object_name = "notes"

class NoteDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note = DoctorNote.objects.select_related('doctor', 'meeting').filter(pk=pk).last()
        if note is not None:
            note.delete()
        messages.success(request, "Successfully deleted!")
        return redirect("notes")

# ********************   MEETING VIEWS ********************

def room(request):
    return render(request, 'room.html')


def getToken(request):
    appId = settings.AGORA_APP_ID
    appCertificate = settings.AGORA_APP_CERT
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid, 'appID': appId}, safe=False)

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=f"{request.user.first_name} {request.user.last_name}",
        uid=data['UID'],
        room_name=data['room_name']
    )
    appointment_request_instance = selectors.appointment_request_list().filter(pk=int(data['appointment_request'])).last()
    doctor = appointment_request_instance.doctor
    patient = appointment_request_instance.owner
    
    filter_meet = Meeting.objects.select_related('appointment_request', 'doctor', 'patient').filter(appointment_request=appointment_request_instance, room_name=data['room_name'], doctor=doctor, patient=patient)
    if filter_meet.count() == 0:
        meet = Meeting.objects.create(appointment_request=appointment_request_instance, room_name=data['room_name'], doctor=doctor, patient=patient, active=True)
        meet.save()
    else:
        meet_obj = filter_meet.last()
        meet_obj.active = True
        meet_obj.save()
    return JsonResponse({'name':f"{request.user.first_name} {request.user.last_name}"}, safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    note = data['note']
    print(f"---------------------------------------{note=}--------------------------------------------")
    member = RoomMember.objects.filter(
        name=f"{request.user.first_name} {request.user.last_name}",
        uid=data['UID'],
        room_name=data['room_name']
    ).last()
    if member is not None:
        member.delete()
    appointment_request_instance = selectors.appointment_request_list().filter(pk=int(data['appointment_request'])).last()
    doctor = appointment_request_instance.doctor
    patient = appointment_request_instance.owner
    meeting = Meeting.objects.select_related('appointment_request', 'doctor', 'patient').filter(appointment_request=appointment_request_instance, room_name=data['room_name'], doctor=doctor, patient=patient)
    print(f"{meeting.count=}")
    if request.user == doctor:
        if meeting.count != 0:
            meet_obj = meeting.last()
            meet_obj.active = False
            meet_obj.save()

            d_note = DoctorNote.objects.select_related('doctor', 'meeting').filter(doctor=meet_obj.doctor, meeting=meet_obj).last()
            print(f"------------------------------------------------------->{d_note=}")
            if d_note == None:
                try:
                    new_d_note = DoctorNote.objects.create(doctor=meet_obj.doctor, meeting=meet_obj, note=note)
                except:
                    print("Except ishe dushdu")
                    pass
            else:
                print("Else ishe dushdu")
                d_note.doctor = meet_obj.doctor
                d_note.meeting = meet_obj
                d_note.note = note
                d_note.save()
    return JsonResponse('Member deleted', safe=False)