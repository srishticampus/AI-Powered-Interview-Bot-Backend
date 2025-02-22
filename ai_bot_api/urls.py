from django.urls import path
from .views import RegisterView,LoginView,UserListView,UserDetailView,AddCompanyView,ResetPasswordView,AddJobView,UserMatchedJobsView,CompaniesListView,CompanyDetailView,JobsListView,JobDetailView,ApplyJobView,UserAppliedJobView,UpdateApplicationStatusView,AllAppliedjobsView,CompanyEditView,DeleteCompanyView,EditJobsView,DeleteJobView,generate_mcqs_from_resume


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
     path('edit-company/<int:company_id>/', CompanyEditView.as_view(), name='edit-company'),
     path('delete-company/<int:company_id>/', DeleteCompanyView.as_view(), name='delete-company'),
     path('jobs/', JobsListView.as_view(), name='job-list'),
     path('job/<int:job_id>/', JobDetailView.as_view(), name='job-detail'),
     path('edit-job/<int:job_id>/', EditJobsView.as_view(), name='edit-job'),
     path('delete-job/<int:job_id>/', DeleteJobView.as_view(), name='delete-job'),
     path('apply-job/',ApplyJobView.as_view(), name='apply-job'),
     path('user-applied-job/<int:user_id>/',UserAppliedJobView.as_view(), name='user-applied-job'),
     path('update-application-status/',UpdateApplicationStatusView.as_view(), name='update-application-status'),
     path('all-applied-jobs/', AllAppliedjobsView.as_view(), name='all-applied-jobs'),
     path("generate-mcqs/<int:user_id>/", generate_mcqs_from_resume, name="generate_mcqs"),
]
