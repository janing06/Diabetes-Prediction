from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from diabetes.models import Diagnosis, Patient, Barangay
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import PatientFrom
from decimal import Decimal
from django.db.models import Q

def diagnos_delete(request, id):
     diagnosis = get_object_or_404(Diagnosis, pk=id)
     
    
    
     diagnosis.delete()
     messages.warning(request, 'Diagnosis Deleted Successfully.')
     return redirect('diagnosis')

def diagnos_update(request, id):
     
     # diagnosis = get_object_or_404(Diagnosis, pk=id)
          
     # if diagnosis.patient.added_by != request.user:
     #     messages.error(request, 'You did not add the Patient')
     #     return redirect('diagnosis')
     
     if request.method == 'POST':
     
          diagnosis = get_object_or_404(Diagnosis, pk=id)
          
          
          patient_id = request.POST.get('patient')
          try:
               patient = get_object_or_404(Patient, pk=patient_id)
          except:
               messages.error(request, 'Please enter correct ID')
               return redirect('diagnosis')
          
          date = request.POST.get('date')
          description = request.POST.get('description')
          current_age = int(request.POST.get('current_age'))
          current_weight = Decimal(request.POST.get('current_weight'))
          test1 = Decimal(request.POST.get('test1'))
          test2 = Decimal(request.POST.get('test2'))
          test3 = Decimal(request.POST.get('test3'))
          
          # Update the existing diagnosis object
          diagnosis.patient = patient
          diagnosis.date = date
          diagnosis.description = description
          diagnosis.current_age = current_age
          diagnosis.current_weight = current_weight
          diagnosis.test1 = test1
          diagnosis.test2 = test2
          diagnosis.test3 = test3
          diagnosis.save()
          
     
          messages.success(request, 'Diagnosis Updated Successfully.')
          return redirect('diagnosis') 
     
     else:
          
     
          diagnosis = get_object_or_404(Diagnosis, pk=id)


          return render(request, 'diabetes/diagnosis-update.html',{'diagnosis': diagnosis})

def patient_list_api(request):
     
     query = request.GET.get('q', '')

     patients = Patient.objects.filter(custom_patient_id__istartswith=query).values('id', 'custom_patient_id').order_by('-custom_patient_id')

     return JsonResponse(list(patients), safe=False)

def diagnos_create(request):

     if request.method == 'POST':
     
          patient_id = request.POST.get('patient')
          try:
               patient = get_object_or_404(Patient, pk=patient_id)
          except:
               messages.error(request, 'Please enter correct ID')
               return redirect('diagnosis-create')
          
          date = request.POST.get('date')
          description = request.POST.get('description')
          current_age = int(request.POST.get('current_age'))
          current_weight = Decimal(request.POST.get('current_weight'))
          test1 = Decimal(request.POST.get('test1'))
          test2 = Decimal(request.POST.get('test2'))
          test3 = Decimal(request.POST.get('test3'))
          
          Diagnosis.objects.create(
               patient=patient,
               date=date,
               description=description,
               current_age=current_age,
               current_weight=current_weight,
               test1=test1,
               test2=test2,
               test3=test3
          )
          
     
          messages.success(request, 'Diagnosis Added Successfully.')
          return redirect('diagnosis') 
          
     else:
          return render(request, 'diabetes/diagnosis-create.html')


def diagnosis_index(request):
     
     search = request.GET.get('search')
     
     if search:
          queryset = Diagnosis.objects.filter(Q(patient__custom_patient_id__icontains=search) | Q(date__icontains=search)).order_by('-updated_at')
     else:
          search = ''
          queryset = Diagnosis.objects.all().order_by('-updated_at')
     
     items_per_page = 5

     paginator = Paginator(queryset, items_per_page)

     page_number = request.GET.get('page')

     diagnosis = paginator.get_page(page_number)
     
     
     return render(request, 'diabetes/diagnosis-index.html',{'diagnosis': diagnosis, 'search': search})


def patient_delete(request, id):
     patient = get_object_or_404(Patient, pk=id)
     
     if patient.added_by != request.user:
         messages.error(request, 'You did not add the Patient')
         return redirect('patients')
    
     patient.delete()
     messages.warning(request, 'Patient Deleted Successfully.')
     return redirect('patients')


def patient_update(request, id):
    # Get the patient object you want to update
    patient = get_object_or_404(Patient, pk=id)
    

    if request.method == 'POST':
        form = PatientFrom(request.POST, instance=patient)
        if form.is_valid():
            # Update the patient object with the new values
            form.save()
            messages.success(request , 'Patient Updated Successfully.')
            return redirect('patients')  # Replace with your success page URL
    else:
        # Initialize the form with the current patient data
        form = PatientFrom(instance=patient)

    return render(request, 'diabetes/patient-update.html', {'form': form,'patient': patient})

@login_required(login_url='/login')
def patient_create(request):
     
     if request.method == 'POST':
          
          form = PatientFrom(request.POST)
          
          if form.is_valid():
               patient = form.save(commit=False)
               
               patient.added_by = request.user

               patient.save()

               messages.success(request, 'Patient Added Successfully.')
               return redirect('patients')
          
     else:     
          form = PatientFrom()
          return render(request, 'diabetes/patient-create.html', {'form': form})

@login_required(login_url='/login')
def patient_index(request):
     
     search = request.GET.get('search')
     
     if search:
          queryset = Patient.objects.filter(Q(custom_patient_id__icontains = search) | Q(first_name__icontains = search) | Q(last_name__icontains = search) | Q(added_by__first_name__icontains=search) | Q(added_by__last_name__icontains=search)).order_by('-created_at')
     else:
          search = ''
          queryset = Patient.objects.all().order_by('-created_at')
     items_per_page = 5

     paginator = Paginator(queryset, items_per_page)

     page_number = request.GET.get('page')

     patients = paginator.get_page(page_number)
     
     return render(request, 'diabetes/patient-index.html',{'patients': patients, 'search': search})




@login_required(login_url='/login')
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
     if not request.user.is_authenticated:
          if request.method == "POST":
               username = request.POST.get('username')
               password = request.POST.get('password')
               user = authenticate(username=username, password=password)
               if user is not None:
                    auth_login(request, user)  # Use auth_login instead of login
                    return redirect('index')
               else:
                    messages.success(request, 'Invalid username or password')
          return render(request, 'diabetes/login.html')
     else:
          return render(request, 'diabetes/index.html')

@login_required(login_url='/login')
def profile(request):
     return render(request, 'diabetes/profile.html')

@login_required
def update_password(request):
     current_password = request.POST.get('current_password')
     new_password = request.POST.get('password')
     confirm_password = request.POST.get('password_confirmation')

     user = request.user
     # Check if the current password is correct
     if not authenticate(username=user.username, password=current_password):
          messages.error(request, 'Incorrect current password.')
          return redirect('profile')  # Change this to your profile view or another suitable URL
          
     else:
          # Check if the new password and confirmation match
          if new_password != confirm_password:
               messages.error(request, 'New password and confirmation do not match.')
               return redirect('profile')  # Change this to your profile view or another suitable URL
          else:
               # Update the user's password
               user.set_password(new_password)
               user.save()
               messages.success(request, 'Your password was successfully updated!')
               auth_login(request, user)  # Log the user back in
               return redirect('profile')  # Change this to your profile view or another suitable URL
