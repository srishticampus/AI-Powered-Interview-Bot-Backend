from django.urls import path
from .views import RegisterView,LoginView,UserListView,UserDetailView,AddCompanyView,ResetPasswordView,AddJobView,UserMatchedJobsView,CompaniesListView,CompanyDetailView,JobsListView,JobDetailView


urlpatterns = [
     path('register/', RegisterView.as_view(), name='register'),
     path('login/', LoginView.as_view(), name='login'),
     path('users/', UserListView.as_view(), name='user-list'),
     path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
     path('addcompany/', AddCompanyView.as_view(), name='addcompany'),
     path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
     path('addjob/', AddJobView.as_view(), name='addjob'),
     path('user/<int:user_id>/matched-jobs/', UserMatchedJobsView.as_view(), name='user-matched-jobs'),
     path('companies/',CompaniesListView.as_view(),name='company-detail'),
     path('company/<int:company_id>/', CompanyDetailView.as_view(), name='company-list'),
     path('jobs/', JobsListView.as_view(), name='job-list'),
     path('job/<int:job_id>/', JobDetailView.as_view(), name='job-detail'),

]
