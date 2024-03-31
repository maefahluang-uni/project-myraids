from django.db import models


# Create your models here.


class DebtorExcelBase(models.Model):

    No = models.IntegerField(unique=False, null=True, verbose_name="num")
    AN = models.IntegerField(unique=False, null=True)
    HN = models.IntegerField(unique=False, null=True)
    CID = models.CharField(max_length=80, unique=False, null=True)
    name = models.CharField(max_length=200, null=True)
    nationality = models.CharField(max_length=30, null=True)
    admit_date = models.DateField(null=True)
    left_date = models.DateField(null=True)
    total_days = models.SmallIntegerField(null=True)
    Pdx = models.CharField(max_length=10, unique=False, null=True)
    AdjRw = models.FloatField(null=True)
    AuthenCode = models.CharField(max_length=30, unique=False, null=True)
    Pttype = models.CharField(max_length=10, null=True)
    claim_catg = models.CharField(max_length=100, null=True)
    claim_folname_code = models.FloatField(null=True)
    claim_folname = models.CharField(max_length=100, null=True)
    claim_catg_code = models.CharField(max_length=20, null=True)
    HospMain = models.CharField(max_length=100, null=True)
    HospSub = models.CharField(max_length=100, null=True)
    p_chart_status = models.CharField(max_length=30, null=True)
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

    No = models.IntegerField(unique=False, null=True, verbose_name="num")
    AN = models.IntegerField(unique=False, null=True)
    HN = models.IntegerField(unique=False, null=True)
    CID = models.CharField(max_length=80, unique=False, null=True)
    name = models.CharField(max_length=200, null=True)
    nationality = models.CharField(max_length=30, null=True)
    admit_date = models.DateField(null=True)
    left_date = models.DateField(null=True)
    total_days = models.SmallIntegerField(null=True)
    Pdx = models.CharField(max_length=10, unique=False, null=True)
    AdjRw = models.FloatField(null=True)
    AuthenCode = models.CharField(max_length=30, unique=False, null=True)
    Pttype = models.CharField(max_length=10, null=True)
    claim_catg = models.CharField(max_length=100, null=True)
    claim_folname_code = models.FloatField(null=True)
    claim_folname = models.CharField(max_length=100, null=True)
    claim_catg_code = models.CharField(max_length=20, null=True)
    HospMain = models.CharField(max_length=100, null=True)
    HospSub = models.CharField(max_length=100, null=True)
    p_chart_status = models.CharField(max_length=30, null=True)
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


class FieldPreset(models.Model):
    name = models.CharField(max_length=100, unique=True)
    preset_data = models.JSONField()

    def __str__(self):
        return self.name