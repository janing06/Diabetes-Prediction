from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
     path('', views.index, name='index'),
     path('login/', views.login, name='login'),
     path('profile/', views.profile, name='profile'),
     path('patients/', views.patient_index, name='patients'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('patient/create/', views.patient_create, name='patient-create'),
     path('patient/update/<int:id>/', views.patient_update, name='patient-update'),
     path('patient/delete/<int:id>/', views.patient_delete, name='patient-delete'),
     path('profile/update-password/', views.update_password, name='update-password'),
     path('patient_api/', views.patient_list_api, name='patient-api'),
     path('diagnosis/', views.diagnosis_index, name='diagnosis'),
     path('diagnosis/create/', views.diagnos_create, name='diagnosis-create'),
     path('diagnosis/update/<int:id>/', views.diagnos_update, name='diagnosis-update'),
     path('diagnosis/delete/<int:id>/', views.diagnos_delete, name='diagnosis-delete'),

]