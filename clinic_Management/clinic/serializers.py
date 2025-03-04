# clinic/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Employee, Patient, PatientNurseDetails, PatientDoctorDetail, LaboratoryPatientDetail, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'patient', 'amount', 'payment_date', 'payment_method', 'transaction_id', 'status', 'created_at', 'updated_at']
        read_only_fields = ['payment_date', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        patient_id = validated_data.get('patient').id if validated_data.get('patient') else self.context.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found")
        
        validated_data['patient'] = patient
        payment = Payment.objects.create(**validated_data)
        # Update patient payment status
        patient.payment_status = True
        patient.save()
        return payment

class LaboratoryPatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryPatientDetail
        fields = ['test_type', 'test_results', 'sample_collected', 'lab_technician', 'updated_at', 'payment_verified']
        read_only_fields = ['lab_technician', 'updated_at', 'payment_verified']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        if request.user.role != 'LabTechnician':
            raise serializers.ValidationError("Only Lab Technicians can add laboratory details")
        
        patient_id = self.context.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found")
        
        if not patient.payment_status:
            raise serializers.ValidationError("Payment for lab tests is required before proceeding")
        
        validated_data['lab_technician'] = request.user
        validated_data['payment_verified'] = True  # Set to True after payment verification
        lab_details, created = LaboratoryPatientDetail.objects.update_or_create(
            patient=patient,
            defaults=validated_data
        )
        return lab_details

class PatientDoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorDetail
        fields = ['diagnosis', 'treatment_plan', 'notes', 'doctor', 'updated_at', 'lab_referral']
        read_only_fields = ['doctor', 'updated_at', 'lab_referral']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        if request.user.role != 'Doctor':
            raise serializers.ValidationError("Only Doctors can add patient doctor details")
        
        patient_id = self.context.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found")
        
        validated_data['doctor'] = request.user
        doctor_details, created = PatientDoctorDetail.objects.update_or_create(
            patient=patient,
            defaults=validated_data
        )
        return doctor_details

class PatientNurseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientNurseDetails
        fields = [
            'pulse_rate', 'respiratory_rate', 'oxygen_saturation', 'weight', 'height',
            'temperature', 'blood_pressure', 'nurse', 'updated_at'
        ]
        read_only_fields = ['nurse', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        if request.user.role != 'Nurse':
            raise serializers.ValidationError("Only Nurses can add patient details")
        
        patient_id = self.context.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found")
        
        validated_data['nurse'] = request.user
        nurse_details, created = PatientNurseDetails.objects.update_or_create(
            patient=patient,
            defaults=validated_data
        )
        return nurse_details

class PatientSerializer(serializers.ModelSerializer):
    nurse_details = PatientNurseDetailsSerializer( read_only=True)
    doctor_details = PatientDoctorDetailSerializer( read_only=True)
    lab_details = LaboratoryPatientDetailSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'grandfather_name', 'sex', 'phone_number',
            'card_no', 'kebele', 'region', 'woreda', 'registration_date', 'symptoms',
            'receptionist', 'nurse', 'doctor', 'lab_technician', 'status', 'created_at',
            'updated_at', 'payment_status', 'nurse_details', 'doctor_details', 'lab_details', 'payments'
        ]
        read_only_fields = ['registration_date', 'created_at', 'updated_at', 'status', 'receptionist', 'nurse', 'doctor', 'lab_technician', 'nurse_details', 'doctor_details', 'lab_details', 'payments']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        if request.user.role != 'Receptionist':
            raise PermissionDenied("Only Receptionists can register patients")
        
        validated_data.pop('nurse_details', None)
        validated_data.pop('doctor_details', None)
        validated_data.pop('lab_details', None)
        validated_data.pop('payments', None)
        
        validated_data['receptionist'] = request.user
        validated_data['status'] = 'PENDING'
        patient = Patient(**validated_data)
        patient.save()
        return patient

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        
        if request.user.role != 'Doctor':
            raise PermissionDenied("Only Doctors can review patient details")
        
        instance.doctor = request.user if request.user.role == 'Doctor' else instance.doctor
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'father_name', 'grandfather_name', 'emp_id', 'gender',
            'body', 'image', 'region', 'zone', 'woreda', 'kebele', 'email', 'phone_number',
            'institution_name', 'field', 'date_of_graduate', 'company_names', 'role',
            'salary', 'pdf', 'licence_type', 'give_date', 'expired_date', 'bank_name',
            'bank_account', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        employee = Employee(**validated_data)
        employee.set_password(password)
        employee.save()
        return employee

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        pdf = validated_data.pop('pdf', None)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.grandfather_name = validated_data.get('grandfather_name', instance.grandfather_name)
        instance.emp_id = validated_data.get('emp_id', instance.emp_id)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.body = validated_data.get('body', instance.body)
        instance.region = validated_data.get('region', instance.region)
        instance.zone = validated_data.get('zone', instance.zone)
        instance.woreda = validated_data.get('woreda', instance.woreda)
        instance.kebele = validated_data.get('kebele', instance.kebele)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.institution_name = validated_data.get('institution_name', instance.institution_name)
        instance.field = validated_data.get('field', instance.field)
        instance.date_of_graduate = validated_data.get('date_of_graduate', instance.date_of_graduate)
        instance.company_names = validated_data.get('company_names', instance.company_names)
        instance.role = validated_data.get('role', instance.role)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.licence_type = validated_data.get('licence_type', instance.licence_type)
        instance.give_date = validated_data.get('give_date', instance.give_date)
        instance.expired_date = validated_data.get('expired_date', instance.expired_date)
        instance.bank_name = validated_data.get('bank_name', instance.bank_name)
        instance.bank_account = validated_data.get('bank_account', instance.bank_account)

        if image is not None:
            instance.image = image
        if pdf is not None:
            instance.pdf = pdf

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}
        if refresh.payload.get('rotating_refresh_token', False):
            data['refresh'] = str(refresh)
        return data