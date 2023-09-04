from django.db import models
from django.contrib.auth.models import User
import uuid

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
     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
     description = models.TextField(blank=True, null=True)
     date = models.DateField()
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     current_age = models.IntegerField(verbose_name='Current Age')
     current_weight = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Current Weight (kg)')
     test1 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Test 1')
     test2 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Test 2')
     test3 = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Test 3')
     prediction_result = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Prediction')
     
     def save(self, *args, **kwargs):
          
          self.prediction_result = self.test1 + self.test2 + self.test3
          
          super(Diagnosis, self).save(*args, **kwargs)
     
     def __str__(self):
          return self.patient.custom_patient_id
     
     class Meta:
          verbose_name_plural = 'Diagnosis'
     
