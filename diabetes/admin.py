from django.contrib import admin
from diabetes.models import ExtendedUserModel, Barangay, Patient, Diagnosis
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ExtendedUserInline(admin.StackedInline):
    model = ExtendedUserModel
    can_delete = False

# Create a custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    inlines = [ExtendedUserInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username']
    
#     list_select_related = ['extendedusermodel']  # Add your ExtendedUserModel here

    def user_image(self, obj):
        # Access the 'image' field from your ExtendedUserModel
        return obj.extendedusermodel.image.url if obj.extendedusermodel and obj.extendedusermodel.image else ''

    user_image.short_description = 'User Image'
    list_per_page = 7

# Register the User model with the custom UserAdmin class
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'municipal']
    ordering = ['name']
    search_fields = ['name']
    
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'middle_name', 'last_name', 'address', 'sex']
    ordering = ['-created_at']
    readonly_fields = ['custom_patient_id', 'created_at', 'updated_at']
    search_fields = ['custom_patient_id']
    autocomplete_fields = ['barangay']

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ['patient', 'current_age', 'current_weight', 'prediction_result']
    autocomplete_fields = ['patient']
    readonly_fields = ['prediction_result']
    ordering = ['-created_at']