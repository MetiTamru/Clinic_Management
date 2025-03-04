# clinic/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee, Patient, PatientNurseDetails, PatientDoctorDetail, LaboratoryPatientDetail, Payment
from .serializers import EmployeeSerializer, LoginSerializer, TokenRefreshSerializer, PatientSerializer, PatientNurseDetailsSerializer, PatientDoctorDetailSerializer, LaboratoryPatientDetailSerializer, PaymentSerializer
from rest_framework.exceptions import PermissionDenied  
from rest_framework_simplejwt.authentication import JWTAuthentication   
from rest_framework.decorators import api_view      
from rest_framework import status
from rest_framework.response import Response        


class PatientDoctorReviewView(generics.UpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'Doctor':
            raise PermissionDenied("Only Doctors can review patient details")
        
        # Check if nurse details are filled before doctor review
        if not instance.nurse_details:
            raise PermissionDenied("Nurse must complete patient details before doctor review")
        
        # Handle doctor-specific details and lab referral
        doctor_details_data = request.data.pop('doctor_details', {})
        lab_referral = request.data.pop('lab_referral', False)
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Update or create doctor details
        instance.doctor = request.user
        instance.save()
        
        # Update or create PatientDoctorDetail
        doctor_details, created = PatientDoctorDetail.objects.get_or_create(
            patient=instance,
            defaults={'doctor': request.user}
        )
        doctor_details_serializer = PatientDoctorDetailSerializer(
            doctor_details,
            data=doctor_details_data,
            partial=True,
            context={'request': request, 'patient_id': instance.id}
        )
        doctor_details_serializer.is_valid(raise_exception=True)
        doctor_details_serializer.save()
        
        # Handle lab referral if requested
        if lab_referral:
            if not instance.payment_status:
                raise PermissionDenied("Payment for lab tests is required before referral")
            instance.status = 'PENDING_PAYMENT'  # Transition to pending payment first
            instance.save()
            return Response({
                'patient': PatientSerializer(instance).data,
                'message': 'Patient referred to laboratory, pending payment'
            }, status=status.HTTP_200_OK)
        
        # Complete patient review if no lab referral
        instance.status = 'COMPLETED'
        instance.save()
        return Response({
            'patient': PatientSerializer(instance).data,
            'message': 'Patient review completed by doctor'
        }, status=status.HTTP_200_OK)

class LaboratoryPatientUpdateView(generics.UpdateAPIView):
    serializer_class = LaboratoryPatientDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LaboratoryPatientDetail.objects.all()

    def get_object(self):
        patient_id = self.kwargs.get('patient_pk')
        try:
            patient = Patient.objects.get(id=patient_id)
            lab_details, created = LaboratoryPatientDetail.objects.get_or_create(patient=patient)
            return lab_details
        except Patient.DoesNotExist:
            raise PermissionDenied("Patient not found")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'LabTechnician':
            raise PermissionDenied("Only Lab Technicians can update laboratory details")
        
        if not instance.patient.payment_status:
            raise PermissionDenied("Payment for lab tests is required before proceeding")
        
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request, 'patient_id': instance.patient.id})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Update patient status to 'COMPLETED' after lab results and payment verification
        instance.patient.lab_technician = request.user
        instance.patient.status = 'COMPLETED'
        instance.patient.save()
        
        return Response({
            'patient': PatientSerializer(instance.patient).data,
            'lab_details': LaboratoryPatientDetailSerializer(instance).data,
            'message': 'Laboratory details updated and patient record completed'
        }, status=status.HTTP_200_OK)

class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise PermissionDenied("Patient not found")
        
        # Check if patient is pending payment for lab
        if patient.status != 'PENDING_PAYMENT':
            raise PermissionDenied("Payment is only required for patients pending lab tests")
        
        serializer = self.get_serializer(data=request.data, context={'patient_id': patient_id, 'request': request})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        
        # Update patient payment status
        patient.payment_status = True
        patient.status = 'PENDING_LAB'  # Transition to pending lab after payment
        patient.save()
        
        return Response({
            'payment': PaymentSerializer(payment).data,
            'patient': PatientSerializer(patient).data,
            'message': 'Payment recorded, patient ready for laboratory analysis'
        }, status=status.HTTP_201_CREATED)

class PatientHistoryView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.all()

    def get_object(self):
        patient_id = self.kwargs.get('pk')
        try:
            patient = Patient.objects.get(id=patient_id)
            # Check if the user has permission to view this patient's history
            user = self.request.user
            if user.role == 'Receptionist' and patient.receptionist != user:
                raise PermissionDenied("You can only view patients you registered")
            elif user.role == 'Nurse' and patient.nurse != user:
                raise PermissionDenied("You can only view patients you handled")
            elif user.role == 'Doctor' and patient.doctor != user:
                raise PermissionDenied("You can only view patients you reviewed")
            elif user.role == 'LabTechnician' and patient.lab_technician != user:
                raise PermissionDenied("You can only view patients you processed")
            return patient
        except Patient.DoesNotExist:
            raise PermissionDenied("Patient not found")

class PatientRegistrationView(generics.CreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'Receptionist':
            raise PermissionDenied("Only Receptionists can register patients")
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        return Response({
            'patient': PatientSerializer(patient).data,
            'message': 'Patient registered and pending nurse review'
        }, status=status.HTTP_201_CREATED)

class PatientNurseUpdateView(generics.UpdateAPIView):
    serializer_class = PatientNurseDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientNurseDetails.objects.all()

    def get_object(self):
        patient_id = self.kwargs.get('patient_pk')
        try:
            patient = Patient.objects.get(id=patient_id)
            nurse_details, created = PatientNurseDetails.objects.get_or_create(patient=patient)
            return nurse_details
        except Patient.DoesNotExist:
            raise PermissionDenied("Patient not found")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'Nurse':
            raise PermissionDenied("Only Nurses can update patient details")
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request, 'patient_id': instance.patient.id})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Update patient status to 'PENDING_DOCTOR' and set the nurse
        instance.patient.nurse = request.user
        instance.patient.status = 'PENDING_DOCTOR'
        instance.patient.save()
        
        # Update nurse in PatientNurseDetails
        instance.nurse = request.user
        instance.save()
        
        return Response({
            'patient': PatientSerializer(instance.patient).data,
            'nurse_details': PatientNurseDetailsSerializer(instance).data,
            'message': 'Patient details updated by nurse and pending doctor review'
        }, status=status.HTTP_200_OK)

class PatientListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Receptionist':
            return Patient.objects.filter(receptionist=user)
        elif user.role == 'Nurse':
            return Patient.objects.filter(nurse=user)
        elif user.role == 'Doctor':
            return Patient.objects.filter(doctor=user)
        elif user.role == 'LabTechnician':
            return Patient.objects.filter(lab_technician=user)
        return Patient.objects.none()

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            employee = Employee.objects.get(email=email)
            if employee.check_password(password):
                refresh = RefreshToken.for_user(employee)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'employee': EmployeeSerializer(employee).data
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Employee.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshView(generics.GenericAPIView):
    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class EmployeeRegistrationView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()
        
        return Response({
            'employee': EmployeeSerializer(employee).data
        }, status=status.HTTP_201_CREATED)

class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.all()

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'employee': EmployeeSerializer(instance).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])

def logout_view(request):
    response = Response({"message": "Logged out successfully"}, status=200)
    response.delete_cookie("jwt")  # Adjust based on your auth setup
    return responses