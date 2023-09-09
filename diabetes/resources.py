from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Diagnosis, Patient

class DiagnosisResource(resources.ModelResource):
     
     patient = fields.Field(column_name='patient_id', attribute='patient', widget=ForeignKeyWidget(Patient, field='custom_patient_id'))
     
     class Meta:
          model = Diagnosis
          fields = ['patient', 'description', 'created_at', 'updated_at', 'current_age', 'current_weight', 'test1', 'test2', 'test3', 'prediction_result']


class PatientResource(resources.ModelResource):
     patient = fields.Field(column_name='patient_id',attribute='custom_patient_id')
     
     class Meta:
          model = Patient
          fields = ['patient_id', 'first_name', 'middle_name', 'last_name', 'sex', 'address', 'created_at', 'updated_at']