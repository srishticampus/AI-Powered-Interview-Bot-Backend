from django.urls import path
from .views import RegisterView,LoginView,UserListView,UserDetailView,AddCompanyView,ResetPasswordView


urlpatterns = [
     path('register/', RegisterView.as_view(), name='register'),
     path('login/', LoginView.as_view(), name='login'),
     path('users/', UserListView.as_view(), name='user-list'),
     path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
     path('addcompany/', AddCompanyView.as_view(), name='addcompany'),
     path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
