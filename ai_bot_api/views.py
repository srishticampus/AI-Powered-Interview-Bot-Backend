from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate
from .models import CustomUser, AddJob, AddCompanies
from .serializers import UserSerializer, AddCompanySerializer, ResetPasswordSerializer, AddJobSerializer
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