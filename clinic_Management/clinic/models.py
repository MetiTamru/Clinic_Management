# clinic/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Receptionist', 'Receptionist'),
        ('Nurse', 'Nurse'),
        ('Doctor', 'Doctor'),
        ('LabTechnician', 'LabTechnician'),
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    grandfather_name = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    region = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    woreda = models.CharField(max_length=100)
    kebele = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    institution_name = models.CharField(max_length=200)
    field = models.CharField(max_length=100)
    date_of_graduate = models.DateField()
    company_names = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Receptionist')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='employee_docs/', blank=True, null=True)
    licence_type = models.CharField(max_length=100)
    give_date = models.DateField()
    expired_date = models.DateField()
    bank_name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'emp_id', 'password', 'role']

    class Meta:
        permissions = []
        default_permissions = ()

    def __str__(self):
        return f"{self.first_name} ({self.emp_id}) - {self.role}"

class Patient(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Review by Nurse'),
        ('IN_PROGRESS', 'In Progress by Nurse'),
        ('PENDING_DOCTOR', 'Pending Review by Doctor'),
        ('PENDING_LAB', 'Pending Laboratory Analysis'),
        ('COMPLETED', 'Completed'),
    )

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grandfather_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    phone_number = models.CharField(max_length=20)
    card_no = models.CharField(max_length=50, unique=True)
    kebele = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    woreda = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    symptoms = models.TextField(blank=True)
    receptionist = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='registered_patients', limit_choices_to={'role': 'Receptionist'})
    nurse = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='assigned_patients', limit_choices_to={'role': 'Nurse'})
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='reviewed_patients', limit_choices_to={'role': 'Doctor'})
    lab_technician = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='lab_patients', limit_choices_to={'role': 'LabTechnician'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"

    class Meta:
        ordering = ['-registration_date']

class PatientNurseDetails(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='nurse_details')
    pulse_rate = models.PositiveIntegerField(blank=True, null=True)
    respiratory_rate = models.PositiveIntegerField(blank=True, null=True)
    oxygen_saturation = models.PositiveIntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    nurse = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='nurse_patient_details', limit_choices_to={'role': 'Nurse'})
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Nurse Details for {self.patient}"

class PatientDoctorDetail(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='doctor_details')
    diagnosis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='doctor_patient_details', limit_choices_to={'role': 'Doctor'})
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Doctor Details for {self.patient}"

class LaboratoryPatientDetail(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='lab_details')
    test_type = models.CharField(max_length=100, blank=True)  # e.g., Blood Test, Urine Test
    test_results = models.TextField(blank=True)  # Results of the test
    sample_collected = models.BooleanField(default=False)
    lab_technician = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='lab_patient_details', limit_choices_to={'role': 'LabTechnician'})
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lab Details for {self.patient}"