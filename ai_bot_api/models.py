from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, blank=False, default="Default Name")
    phone_number = models.CharField(max_length=15, unique=False)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    email = models.EmailField(unique=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True) 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class AddCompanies(models.Model):
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)
    company_email = models.EmailField(unique=True)
    company_phone = models.CharField(max_length=15, unique=False)
    industry_type = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.company_name

class AddJob(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.ForeignKey(AddCompanies, on_delete=models.CASCADE)
    required_skills = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=255)
    job_description = models.TextField()
    application_deadline = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.job_title
    
class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(AddJob, on_delete=models.CASCADE)
    applied_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=125, choices=[
        ("pending", "pending"),
        ("rejected", "rejected"),
        ("shortlisted", "shortlisted"),
        ("technical_interview", "technical_interview"),
        ("technical_interview_completed", "technical_interview_completed"),
        ("technical_interview_rejected", "technical_interview_rejected"),
        ("hr_interview", "hr_interview"),
        ("hr_interview_rejected", "hr_interview_rejected"),
        ("hired", "hired"),
        ("interview_completed", "interview_completed")
        ],
        default="pending")
    score = models.IntegerField(default=-1)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title}"   
    
class ExamScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application = models.ForeignKey('JobApplication', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.application.job.job_title} - Score: {self.score}"