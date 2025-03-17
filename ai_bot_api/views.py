
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
import os
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PyPDF2 import PdfReader
import google.generativeai as genai
from django.shortcuts import get_object_or_404

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
    
class DeteleUserView(APIView):
    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return Response({"message":"user deleted successfully"}, status=status.HTTP_200_OK)

class AddCompanyView(APIView):
    def post(self, request):
        serializer = AddCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddJobView(APIView):
    def post(self, request):
        request.data["company_name"] = request.data.get("company_name") 

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
        jobs = AddJob.objects.all().select_related('company_name')
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

        if new_status not in ['rejected', 'shortlisted', 'technical_interview', 'technical_interview_completed', 'technical_interview_rejected', 'hr_interview', 'hr_interview_rejected', 'hired']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        application = get_object_or_404(JobApplication, id=application_id)
        application.status = new_status
        application.save()

        serializer = JobApplicationSerializer(application)
        return Response({
            "message": f"Application {new_status} successfully",
            "application": serializer.data
        }, status=status.HTTP_200_OK)

    
class AllAppliedjobsView(APIView):
    def get(self, request):
        applications = JobApplication.objects.all()
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AppliedDetailView(APIView):
    def get(self, request, application_id):
        application = get_object_or_404(JobApplication, id=application_id)
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class CompanyEditView(APIView):
    def patch(self, request, company_id):
        company = get_object_or_404(AddCompanies, id=company_id)
        serializer = AddCompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCompanyView(APIView):
    def delete(self, request, company_id):
        company = get_object_or_404(AddCompanies, id=company_id)
        company.delete()
        return Response({"message":"company deleted successfully"}, status=status.HTTP_200_OK)
    
class EditJobsView(APIView):
    def patch(self, request, job_id):
        job = get_object_or_404(AddJob, id=job_id)
        serializer = AddJobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteJobView(APIView):
    def delete(self, request, job_id):
        job = get_object_or_404(AddJob, id=job_id)
        job.delete()
        return Response({"message":"job deleted successfully"}, status=status.HTTP_200_OK)
    
class UpdateScoreView(APIView):
    def post(self, request, application_id):
        score = request.data.get('score')

        if score is None or not isinstance(score, int):
            return Response({"error": "Invalid score"}, status=status.HTTP_400_BAD_REQUEST)

        application = get_object_or_404(JobApplication, id=application_id)
        application.score = score
        application.save()

        return Response({"message": "Score updated successfully", "score": application.score}, status=status.HTTP_200_OK)

# Configure Gemini API key
genai.configure(api_key="AIzaSyBY0bcSaO-DK3A72g0GhdzNCWk6I_1RSqo")

# MCQ storage folder
MCQ_FOLDER = os.path.join(settings.MEDIA_ROOT, "mcq_questions")
os.makedirs(MCQ_FOLDER, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF resume."""
    pdf_reader = PdfReader(pdf_path)
    text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
    return text.strip()


def gemini_request(prompt):
    """Send a request to Gemini AI and return response text."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)

    try:
        return response.text.strip()
    except (AttributeError, IndexError):
        return "Error: Unable to process request."


def suggest_job_titles(text):
    """Extracts job titles from Gemini response and returns a cleaned list."""
    query = f"Suggest job roles that best match the following resume. Rank them from most relevant to least relevant:\n\n{text}"
    
    response = gemini_request(query)

    # Extract job titles (ignoring headers like 'Tier 1', 'Tier 2', etc.)
    job_titles = re.findall(r"^\d*\.*\s*\*\*(.*?)\*\*", response, re.MULTILINE)

    # Remove tier headers (like 'Tier 1: Most Relevant')
    filtered_titles = [title for title in job_titles if not re.match(r"^Tier\s*\d+", title, re.IGNORECASE)]

    if filtered_titles:
        return [title.strip().rstrip(":") for title in filtered_titles if title.strip()]
    
    return []


def generate_mcq_questions(job_title, difficulty="Medium"):
    """Generates 15 technical and 15 aptitude MCQs for a given job title."""


    tech_query = f"""
    Generate 15 multiple-choice technical interview questions for the job title '{job_title}' with {difficulty} difficulty.
    
    Format output in JSON as:
    [
      {{"id": 1, "question": "Tech Question 1?", "option1": "A", "option2": "B", "option3": "C", "option4": "D", "answer": "option2", "type": "Technical"}},
      ...
    ]
    """
    tech_response = gemini_request(tech_query)
    tech_questions = extract_json(tech_response)

    # Request Aptitude Questions
    aptitude_query = f"""
    Generate 15 multiple-choice aptitude test questions relevant to the job title '{job_title}' with {difficulty} difficulty.
    
    Format output in JSON as:
    [
      {{"id": 16, "question": "Aptitude Question 1?", "option1": "A", "option2": "B", "option3": "C", "option4": "D", "answer": "option1", "type": "Aptitude"}},
      ...
    ]
    """
    aptitude_response = gemini_request(aptitude_query)
    aptitude_questions = extract_json(aptitude_response)

    for idx, question in enumerate(aptitude_questions, start=len(tech_questions) + 1):
        question["id"] = idx

   
    mcq_questions = tech_questions + aptitude_questions

    return mcq_questions if len(mcq_questions) == 30 else []


def extract_json(text):
    """Extracts JSON content from AI response."""
    match = re.search(r"\[\s*{.*}\s*\]", text, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else []
    except json.JSONDecodeError:
        return []


def save_json_file(content, job_title):
    """Saves generated MCQs into a JSON file."""
    safe_title = re.sub(r"[^a-zA-Z0-9_]", "_", job_title)
    filename = os.path.join(MCQ_FOLDER, f"{safe_title}_mcqs.json")

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(content, file, indent=4)

    return filename


@csrf_exempt
def generate_mcqs_from_resume(request, user_id):
    """API to generate MCQs from a user's resume."""
    user = get_object_or_404(CustomUser, id=user_id)

    if not user.resume:
        return JsonResponse({"error": "No resume found for this user"}, status=404)

    resume_path = os.path.join(settings.MEDIA_ROOT, str(user.resume))

    try:
        resume_text = extract_text_from_pdf(resume_path)
        job_titles = suggest_job_titles(resume_text)



        if not job_titles:
            return JsonResponse({"error": "Failed to identify suitable job roles"}, status=400)

        
        
        preferred_job_title = job_titles[1]
        mcqs = generate_mcq_questions(preferred_job_title)

        if mcqs:
            return JsonResponse({"job_title": preferred_job_title, "mcqs": mcqs}, status=200)
        else:
            return JsonResponse({"error": "Failed to generate MCQs"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def get_mcq_file(request, filename):
    """API to download the generated MCQ JSON file."""
    file_path = os.path.join(MCQ_FOLDER, filename)

    if not os.path.exists(file_path):
        return JsonResponse({"error": "File not found"}, status=404)

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return JsonResponse({"mcqs": data})

import cv2
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io

# Load Model and Face Detector
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('model3.h5')
emotion_labels = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

class EmotionDetectionView(APIView):
    def post(self, request):
        image_file = request.FILES.get("image")

        if not image_file:
            return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert Image File to OpenCV Format
        image_stream = io.BytesIO(image_file.read())
        image_pil = Image.open(image_stream).convert("RGB")
        image_np = np.array(image_pil)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Convert to Grayscale
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) == 0:
            return Response({"error": "No face detected"}, status=status.HTTP_400_BAD_REQUEST)

        # Process Detected Faces
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            roi = roi_gray.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]

            return Response({"emotion": label}, status=status.HTTP_200_OK)

        return Response({"error": "Face processing failed"}, status=status.HTTP_400_BAD_REQUEST)
