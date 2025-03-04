# clinic/urls.py
from django.urls import path
from .views import EmployeeRegistrationView, LoginView, TokenRefreshView, EmployeeListView, EmployeeDetailView, PatientRegistrationView, PatientNurseUpdateView, PatientDoctorReviewView, PatientListView, PatientHistoryView, LaboratoryPatientUpdateView, PaymentCreateView

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name='employee-register'),
    path('login/', LoginView.as_view(), name='employee-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('patients/register/', PatientRegistrationView.as_view(), name='patient-register'),
    path('patients/<int:patient_pk>/nurse/', PatientNurseUpdateView.as_view(), name='patient-nurse-update'),
    path('patients/<int:pk>/doctor/', PatientDoctorReviewView.as_view(), name='patient-doctor-review'),
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/history/', PatientHistoryView.as_view(), name='patient-history'),
    path('patients/<int:patient_pk>/lab/', LaboratoryPatientUpdateView.as_view(), name='patient-lab-update'),
    path('patients/<int:patient_pk>/payment/', PaymentCreateView.as_view(), name='patient-payment-create'),
]