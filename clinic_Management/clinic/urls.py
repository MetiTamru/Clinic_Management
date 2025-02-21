# clinic/urls.py
from django.urls import path
from .views import EmployeeListView , EmployeeDetailView, EmployeeRegistrationView, LoginView, TokenRefreshView, PasswordResetRequestView, PasswordResetConfirmView 

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name='employee-register'),
    path('login/', LoginView.as_view(), name='employee-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
]