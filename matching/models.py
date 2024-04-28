from django.db import models
from django.conf import settings
import os
from datetime import datetime


# Create your models here.
class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)

class Profile (models.Model):
    user = models.OneToOneField(CustomUser,primary_key=True,on_delete=models.CASCADE)

def debtor_upload_path(instance, filename):
    return os.path.join ('uploads', "debtor",filename)    

def claimer_upload_path(instance, filename):
    return os.path.join ("uploads", "claimer" , filename)

class ExcelFile(models.Model):
    id = models.AutoField(primary_key=True)
    debtor_file = models.FilePathField(path=debtor_upload_path, recursive=True, match=".xlsx")
    claimer_file = models.FilePathField(path=claimer_upload_path,recursive=True,match=".xlsx")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Preset (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    admin_file = models.OneToOneField(ExcelFile,on_delete=models.CASCADE, related_name= 'admin_preset')
    debtor_file= models.OneToOneField(ExcelFile,on_delete = models.CASCADE, related_name = "debtor_preset")
    claimer_file = models.OneToOneField(ExcelFile,on_delete=models.CASCADE,related_name="claimer_preset")
    ceo_file = models.OneToOneField(ExcelFile, on_delete=models.CASCADE, related_name="ceo_preset")
    debtor_mapping = models.JSONField(null=True)
    claimer_mapping = models.JSONField(null=True)


class DebtorExcelBase(models.Model):
    id = models.AutoField(primary_key=True)
    No = models.IntegerField(unique=False, null=True,)
    common_column = models.CharField(max_length=100)
    HN = models.IntegerField(unique=False, null=True)
    CID = models.CharField(max_length=80, unique=False, null=True)
    name = models.CharField(max_length=200, null=True)
    nationality = models.CharField(max_length=50, null=True)
    admit_date = models.DateField(null=True)
    left_date = models.DateField(null=True)
    total_days = models.SmallIntegerField(null=True)
    Pdx = models.CharField(max_length=10, unique=False, null=True)
    AdjRw = models.FloatField(null=True)
    AuthenCode = models.CharField(max_length=50, unique=False, null=True)
    Pttype = models.CharField(max_length=10, null=True)
    claim_catg = models.CharField(max_length=100, null=True)
    claim_folname_code = models.FloatField(null=True)
    claim_folname = models.CharField(max_length=100, null=True)
    claim_catg_code = models.CharField(max_length=20, null=True)
    HospMain = models.CharField(max_length=100, null=True)
    HospSub = models.CharField(max_length=100, null=True)
    p_chart_status = models.CharField(max_length=50, null=True)
    expense_fee = models.FloatField(null=True)
    amount_tobe_paid_fee = models.FloatField(null=True)
    amount_paid_fee = models.FloatField(null=True)
    debt_left_fee = models.FloatField(null=True)
    room_food_fee = models.FloatField(null=True)
    prosthetic_fee = models.FloatField(null=True)
    drug_fee = models.FloatField(null=True)
    takehome_drug_fee = models.FloatField(null=True)
    medical_supplie_fee = models.FloatField(null=True)
    bloodcomponent_fee = models.FloatField(null=True)
    Lab_fee = models.FloatField(null=True)
    X_Ray_fee = models.FloatField(null=True)
    special_inspection_fee = models.FloatField(null=True)
    equipment_fee = models.FloatField(null=True)
    procedure_fee = models.FloatField(null=True)
    nursing_fee = models.FloatField(null=True)
    dental_fee = models.FloatField(null=True)
    physicaltharapy_fee = models.FloatField(null=True)
    othertharapy_fee = models.FloatField(null=True)
    other_fee = models.FloatField(null=True)
    not_insure_fee = models.FloatField(null=True)
    doctor_fee = models.FloatField(null=True)
    total_fee = models.FloatField(null=True)


class ClaimerExcelBase(models.Model):
    id = models.AutoField(primary_key=True)
    common_column = models.CharField(max_length=100,null= True)
    Stat = models.CharField(max_length=100,null= True)
    Ext = models.FloatField(null= True)
    line = models.CharField(max_length=100, null= True)
    Herg = models.FloatField(null= True)
    HN = models.CharField(max_length=100,null= True)
    SessNo = models.CharField(max_length=100,null= True)
    BegHd = models.CharField(max_length=100,null= True)
    HdMode = models.CharField(max_length=100,null= True)
    ClaimAcc = models.CharField(max_length=100,null= True)
    Payers = models.CharField(max_length=100,null= True)
    Ep = models.CharField(max_length=100,null= True)
    DizNew = models.CharField(max_length=100,null= True)
    Amount = models.CharField(max_length=100,null= True)
    HDrate = models.CharField(max_length=100,null= True)
    NetTotal = models.CharField(max_length=100,null= True)
    importdate = models.CharField(max_length=100,null= True)
    importstaff = models.CharField(max_length=100,null= True)
    bill = models.CharField(max_length=100,null= True)


class FieldPreset(models.Model):
    name = models.CharField(max_length=100, unique=True)
    preset_data = models.JSONField()

    def __str__(self):
        return self.name