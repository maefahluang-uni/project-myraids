from django.db import models
from django.contrib.auth.models import User
from .storage import NumberedFileSystemStorage
from .forms import LOCATION_CHOICES, PATIENT_TYPE_CHOICES

numbered_storage = NumberedFileSystemStorage()

# ExcelFile model
class ExcelFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, choices=LOCATION_CHOICES)
    patient_type = models.CharField(max_length=30, choices=PATIENT_TYPE_CHOICES)
    file = models.FileField(upload_to='filestorage',storage=numbered_storage)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name.split('/')[-1]}"

# Debtor model
class Debtor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    excelfile = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, related_name='debtors',null=True)  # Corrected ForeignKey
    No = models.CharField(max_length=50)
    VN = models.CharField(max_length=50)
    HN = models.CharField(max_length=50)
    CID = models.CharField(max_length=50)
    PatientName = models.CharField(max_length=500)
    sex = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    National = models.CharField(max_length=100)
    vstdate = models.CharField(max_length=50)
    vsttime = models.CharField(max_length=50)
    Pdx = models.CharField(max_length=50)
    AuthenCode = models.CharField(max_length=50)
    Pttype = models.CharField(max_length=50)
    PttypeName = models.CharField(max_length=500)
    AccCode = models.CharField(max_length=50)
    AccName = models.CharField(max_length=500)
    Pttype_number = models.CharField(max_length=50)
    HospMain = models.CharField(max_length=100)
    HospSub = models.CharField(max_length=100)
    Price = models.CharField(max_length=50)
    MustPay = models.CharField(max_length=50)
    Paid = models.CharField(max_length=50)
    debt = models.CharField(max_length=50)
    room_food = models.CharField(max_length=50)
    Artificial = models.CharField(max_length=50)
    medicine = models.CharField(max_length=50)
    Home_Med = models.CharField(max_length=50)
    Med_sup = models.CharField(max_length=50)
    Blood_Components = models.CharField(max_length=50)
    Lab = models.CharField(max_length=50)
    X_Ray = models.CharField(max_length=50)
    Extra = models.CharField(max_length=50)
    Equipment = models.CharField(max_length=50)
    surgery = models.CharField(max_length=50)
    nurse_serv = models.CharField(max_length=50)
    dental = models.CharField(max_length=50)
    physical = models.CharField(max_length=50)
    other_treatment = models.CharField(max_length=50)
    other_cost = models.CharField(max_length=50)
    med_extra = models.CharField(max_length=50)
    doctor_cost = models.CharField(max_length=50)
    cost = models.CharField(max_length=50)
    DoctorName = models.CharField(max_length=500)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    patient_type = models.CharField(max_length=50, choices=PATIENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.PatientName} ({self.HN})"


# Claimer model
class Claimer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    excelfile = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, related_name='claimers',null=True)  # Corrected ForeignKey
    VN = models.CharField(max_length=50)
    HN = models.CharField(max_length=50)
    Stat = models.CharField(max_length=50)
    Ext = models.CharField(max_length=50)
    Line = models.CharField(max_length=50)
    Hreg = models.CharField(max_length=50)
    SessNo = models.CharField(max_length=50)
    BegHd = models.CharField(max_length=50)
    HdMode = models.CharField(max_length=50)
    ClaimAcc = models.CharField(max_length=50)
    Payers = models.CharField(max_length=50)
    Ep = models.CharField(max_length=50)
    DlzNew = models.CharField(max_length=50)
    Amount = models.CharField(max_length=50)
    HDrate = models.CharField(max_length=50)
    NetTotal = models.CharField(max_length=50)
    importdate = models.CharField(max_length=50)
    importStaff = models.CharField(max_length=50)
    bill = models.CharField(max_length=50)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    patient_type = models.CharField(max_length=50, choices=PATIENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.VN} ({self.HN})"
