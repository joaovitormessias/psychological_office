from django.contrib import admin

from .models import Patient, User, Appointment, Consultation

#------------------------ ADMIN PANEL ------------------------#


#Register Patient model
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'patient_name', 'dob')

#Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email')

#Register Appointment model
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'time', 'status')

#Register Consultation model
@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'status')