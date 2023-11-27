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
from django.utils import timezone
from datetime import datetime
import json
from django.db.models.functions import TruncYear, TruncMonth
from django.db.models import Count, F
import calendar



@login_required(login_url='/login')
def diagnos_delete(request, id):
     diagnosis = get_object_or_404(Diagnosis, pk=id)
     
    
    
     diagnosis.delete()
     messages.warning(request, 'Diagnosis Deleted Successfully.')
     return redirect('diagnosis')


@login_required(login_url='/login')
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
          current_age = int(float(request.POST.get('current_age')))
          current_weight = float(request.POST.get('current_weight'))
          test_pregnancies = int(float(request.POST.get('test_pregnancies')))
          test_glucose = int(float(request.POST.get('test_glucose')))
          test_blood_pressure = int(float(request.POST.get('test_blood_pressure')))
          test_skin_thickness = int(float(request.POST.get('test_skin_thickness')))
          test_insulin = int(float(request.POST.get('test_insulin')))
          test_bmi = float(request.POST.get('test_bmi'))
          test_diabetes_pedigree_function = float(request.POST.get('test_diabetes_pedigree_function'))
          
          diagnosis.patient = patient
          diagnosis.date = date
          diagnosis.description = description
          diagnosis.current_age = current_age
          diagnosis.current_weight = current_weight
          diagnosis.test_pregnancies = test_pregnancies
          diagnosis.test_glucose = test_glucose
          diagnosis.test_blood_pressure = test_blood_pressure
          diagnosis.test_skin_thickness = test_skin_thickness
          diagnosis.test_insulin = test_insulin
          diagnosis.test_bmi = test_bmi
          diagnosis.test_diabetes_pedigree_function = test_diabetes_pedigree_function
          diagnosis.save()
          
     
          messages.success(request, 'Diagnosis Updated Successfully.')
          return redirect('diagnosis') 
     
     else:
          
     
          diagnosis = get_object_or_404(Diagnosis, pk=id)


          return render(request, 'diabetes/diagnosis-update.html',{'diagnosis': diagnosis})


@login_required(login_url='/login')
def patient_list_api(request):
     
     query = request.GET.get('q', '')

     patients = Patient.objects.filter(custom_patient_id__istartswith=query).values('id', 'custom_patient_id').order_by('-custom_patient_id')

     return JsonResponse(list(patients), safe=False)


@login_required(login_url='/login')
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
          current_age = request.POST.get('current_age')
          current_weight = float(request.POST.get('current_weight'))
          test_pregnancies = request.POST.get('test_pregnancies')
          test_glucose = request.POST.get('test_glucose')
          test_blood_pressure = request.POST.get('test_blood_pressure')
          test_skin_thickness = request.POST.get('test_skin_thickness')
          test_insulin =request.POST.get('test_insulin')
          test_bmi = float(request.POST.get('test_bmi'))
          test_diabetes_pedigree_function = float(request.POST.get('test_diabetes_pedigree_function'))
          
          Diagnosis.objects.create(
               added_by=request.user,
               patient=patient,
               date=date,
               description=description,
               current_age=int(float(current_age)),
               current_weight=current_weight,
               test_pregnancies=int(float(test_pregnancies)),
               test_glucose=int(float(test_glucose)),
               test_blood_pressure=int(float(test_blood_pressure)),
               test_skin_thickness=int(float(test_skin_thickness)),
               test_insulin=int(float(test_insulin)),
               test_bmi=test_bmi,
               test_diabetes_pedigree_function=test_diabetes_pedigree_function,
          )
          
     
          messages.success(request, 'Diagnosis Added Successfully.')
          return redirect('diagnosis') 
          
     else:
          return render(request, 'diabetes/diagnosis-create.html')


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def patient_delete(request, id):
     patient = get_object_or_404(Patient, pk=id)
     
     if patient.added_by != request.user:
         messages.error(request, 'You did not add the Patient')
         return redirect('patients')
    
     patient.delete()
     messages.warning(request, 'Patient Deleted Successfully.')
     return redirect('patients')


@login_required(login_url='/login')
def patient_update(request, id):
    # Get the patient object you want to update
    patient = get_object_or_404(Patient, custom_patient_id=id)
    
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
          queryset = Patient.objects.filter(Q(custom_patient_id__icontains = search) | Q(first_name__icontains = search) | Q(last_name__icontains = search) | Q(added_by__first_name__icontains=search) | Q(added_by__last_name__icontains=search) | Q(barangay__name__icontains=search)).order_by('-created_at')
     else:
          search = ''
          queryset = Patient.objects.all().order_by('-created_at')
     items_per_page = 5

     paginator = Paginator(queryset, items_per_page)

     page_number = request.GET.get('page')

     patients = paginator.get_page(page_number)
     
     return render(request, 'diabetes/patient-index.html',{'patients': patients, 'search': search})



def login(request):
     if not request.user.is_authenticated:
          if request.method == "POST":
               username = request.POST.get('username').strip()
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


@login_required(login_url='/login')
def index(request):
     
     current_year = datetime.now().year
     
     
     diagnos = Diagnosis.objects.all()
     current_year_diagnoses = Diagnosis.objects.filter(date__year=current_year)
     
     yearly_diagnosed = Diagnosis.objects.all().annotate(year=TruncYear('date')).values('year').annotate(total=Count('id')).order_by('year')

     data_yearly = [{'date': item['year'].year, 'total': item['total']} for item in yearly_diagnosed]

     json_yearly_diagnosed = json.dumps(data_yearly)
     
     
     
     monthly_this_year_diagnosed = Diagnosis.objects.filter(date__year=current_year).annotate(month=TruncMonth('date')).values('month').annotate(total=Count('id')).order_by('month')

     data_monthly_this_year = [{'date': item['month'].strftime('%B'), 'total': item['total']} for item in monthly_this_year_diagnosed]
     
     all_months = [calendar.month_name[i] for i in range(1, 13)]
     
     
     
     # Extract the month names from data_monthly_this_year
     existing_months = [item['date'] for item in data_monthly_this_year]

     # Check which months are not present
     missing_months = [month for month in all_months if month not in existing_months]



     # Add missing months to data_monthly_this_year with total set to zero
     for month in missing_months:
          data_monthly_this_year.append({'date': month, 'total': 0})
          
     data_monthly_this_year = sorted(data_monthly_this_year, key=lambda x: list(calendar.month_name).index(x['date']))
               


     json_monthly_this_year_diagnosed = json.dumps(data_monthly_this_year)
     
     
     
     positive_count = Diagnosis.objects.filter(prediction_result=True).count()
     negative_count = Diagnosis.objects.filter(prediction_result=False).count()
     
     positive_count_yearly = Diagnosis.objects.filter(prediction_result=True, date__year=current_year).count()
     negative_count_yearly = Diagnosis.objects.filter(prediction_result=False, date__year=current_year).count()
          
     
     users = User.objects.all()
     patients = Patient.objects.all()
     

     from django.db.models import Min
     
     min_age = Diagnosis.objects.aggregate(min_age=Min('current_age'))

     print(min_age)


     
     return render(request, 'diabetes/index.html',{
          'diagnos': diagnos,
          'users': users,
          'patients': patients,
          'current_year_diagnoses': current_year_diagnoses,
          'json_yearly_diagnosed': json_yearly_diagnosed,
          'json_monthly_this_year_diagnosed': json_monthly_this_year_diagnosed,
          'positive_count': positive_count,
          'negative_count': negative_count,
          'positive_count_yearly': positive_count_yearly,
          'negative_count_yearly': negative_count_yearly,
          'current_year': current_year,
          })