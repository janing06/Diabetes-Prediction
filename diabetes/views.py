from django.shortcuts import render
from django.http import HttpResponse
from diabetes.models import Diagnosis, Patient
from django.contrib.auth.models import User

def cases(request):
     return render(request, 'diabetes/cases.html')

def users(request):
     return render(request, 'diabetes/users.html')

def index(request):
     diagnos = Diagnosis.objects.all()
     users = User.objects.all()
     patients = Patient.objects.all()
     return render(request, 'diabetes/index.html',{
          'diagnos': diagnos,
          'users': users,
          'patients': patients,
          })

def login(request):
     return render(request, 'diabetes/login.html')

def profile(request):
     return render(request, 'diabetes/profile.html')