from django.shortcuts import render

#------------------------ VIEWS ------------------------#

from rest_framework import viewsets
from .models import Patient, Appointment, Consultation
from .serializers import PatientSerializer, AppointmentSerializer, ConsultationSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer