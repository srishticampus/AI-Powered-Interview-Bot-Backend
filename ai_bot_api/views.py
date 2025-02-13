from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate
from .models import CustomUser, AddJob, AddCompanies
from .serializers import UserSerializer, AddCompanySerializer, ResetPasswordSerializer, AddJobSerializer, JobApplication, JobApplicationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            return Response({'message': 'Login successful',"user_id": user.id}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all() 
        serializer = UserSerializer(users, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK) 

class UserDetailView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddCompanyView(APIView):
    def post(self, request):
        serializer = AddCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddJobView(APIView):
    def post(self, request):
        serializer = AddJobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserMatchedJobsView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        if not user.skills:
            return Response({"message": "User does not have any skills."}, status=status.HTTP_400_BAD_REQUEST)

        user_skills = set(user.skills.split(","))

        matching_jobs = []
        all_jobs = AddJob.objects.all()

        for job in all_jobs:
            if job.required_skills:
                job_skills = set(job.required_skills.split(","))
                if user_skills & job_skills:
                    matching_jobs.append(job)

        serializer = AddJobSerializer(matching_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CompaniesListView(APIView):
    def get(self, request):
        companies = AddCompanies.objects.all()
        serializer = AddCompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CompanyDetailView(APIView):
    def get(self, request, company_id):
        company = get_object_or_404(AddCompanies, id=company_id)
        serializer = AddCompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JobsListView(APIView):
    def get(self, request):
        jobs = AddJob.objects.all()
        serializer = AddJobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class JobDetailView(APIView):
        def get(self, request, job_id):
            job = get_object_or_404(AddJob, id=job_id)
            serializer = AddJobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class ApplyJobView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        job_id = request.data.get('job_id')

        user = get_object_or_404(CustomUser, id=user_id)
        job = get_object_or_404(AddJob, id=job_id)

        if JobApplication.objects.filter(user=user, job=job).exists():
            return Response({'message':'already applied for this job'}, status=status.HTTP_400_BAD_REQUEST)
        
        application = JobApplication.objects.create(user=user, job=job)
        return Response({'message':'job application is submitted'}, status=status.HTTP_201_CREATED)
    

class UserAppliedJobView(APIView):
    def get(self, request, user_id):
        applications = JobApplication.objects.filter(user_id=user_id)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateApplicationStatusView(APIView):
    def post(self, request):
        application_id = request.data.get('application_id')
        new_status = request.data.get('status')

        if new_status not in ['accepted', 'rejected']:
            return Response({"error":"invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        application = get_object_or_404(JobApplication, id=application_id)
        application.status = new_status
        application.save()

        return Response({"message":f"application {new_status} successfully"}, status=status.HTTP_200_OK)