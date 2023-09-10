from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from pathlib import Path
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import classification_report



class ExtendedUserModel(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE);
     image = models.ImageField(upload_to='user/images', null=True, blank=True)
     
     def __str__(self):
          return self.user.username
     
     class Meta:
          verbose_name = 'User Image'
          
          
class Barangay(models.Model):
     name = models.CharField(max_length=255)
     code = models.CharField(max_length=11 , unique=True)
     municipal = models.CharField(max_length=255)
     
     def __str__(self):
          return self.name

     class Meta:
          verbose_name_plural = 'Barangay'


def generate_unique_id():
    unique_id = str(uuid.uuid4().int)[:12]  # 12 digits long
    formatted_id = '-'.join([unique_id[i:i+4] for i in range(0, len(unique_id), 4)])
    while Patient.objects.filter(custom_patient_id=formatted_id).exists():
        unique_id = str(uuid.uuid4().int)[:12]  # 12 digits long
        formatted_id = '-'.join([unique_id[i:i+4] for i in range(0, len(unique_id), 4)])
    return formatted_id 
  
  
     
class Patient(models.Model):
     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     custom_patient_id = models.CharField(max_length=14, unique=True, default=generate_unique_id, verbose_name='Patient ID')
     first_name = models.CharField(max_length=255, verbose_name='First name')
     middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Middle name')
     last_name = models.CharField(max_length=255, verbose_name='Last name')
     sex = models.CharField(max_length=1,choices=(('M','M'),('F','F')))
     address = models.CharField(max_length=255, null=True, blank=True)
     barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
     def __str__(self):
          return self.custom_patient_id

     
class Diagnosis(models.Model):
     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
     description = models.TextField(blank=True, null=True)
     date = models.DateField()
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     current_age = models.IntegerField(verbose_name='Current Age')
     current_weight = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Current Weight (kg)')
     test_pregnancies = models.IntegerField(verbose_name='Pregnancies')
     test_glucose = models.IntegerField(verbose_name='Glocuse')
     test_blood_pressure = models.IntegerField(verbose_name='Blood Pressure')
     test_skin_thickness = models.IntegerField(verbose_name='Skin Thickness')
     test_insulin = models.IntegerField(verbose_name='Insulin')
     test_bmi = models.DecimalField(decimal_places=1, max_digits=5 ,verbose_name='BMI')
     test_diabetes_pedigree_function = models.DecimalField(decimal_places=3, max_digits=5 ,verbose_name='Diabetes Pedigree Function')
     prediction_result = models.BooleanField(null=True, blank=True, verbose_name='Prediction')
     
     def save(self, *args, **kwargs):

          model_file_path = Path(settings.BASE_DIR) / 'diabetes' / 'trained_model_diabetes' / 'diabetes-prediction-model.pkl'
          
          model = joblib.load(model_file_path)
          
          result = model.predict([[self.test_pregnancies, self.test_glucose, self.test_blood_pressure, self.test_skin_thickness, self.test_insulin, self.test_bmi, self.test_diabetes_pedigree_function, self.current_age]])

          print(result[0])
          
          if result[0] == 1:
               self.prediction_result = True
          elif result[0] == 0:
               self.prediction_result = False
          else:
               self.prediction_result = ''
          super(Diagnosis, self).save(*args, **kwargs)
     
     def __str__(self):
          return self.patient.custom_patient_id
     
     class Meta:
          verbose_name_plural = 'Diagnosis'
     
