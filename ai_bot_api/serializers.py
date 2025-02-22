from rest_framework import serializers
from .models import CustomUser,AddCompanies,AddJob,JobApplication
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    resume = serializers.FileField(required=False, allow_null=True)
    skills = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number', 'profile_image','resume', 'skills']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        if 'resume' in attrs and attrs['resume']:
            if not attrs['resume'].name.endswith('.pdf'):
                raise serializers.ValidationError({"resume": "Only PDF files are allowed."})
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            profile_image=validated_data.get('profile_image'),
            resume=validated_data.get('resume'),
            skills=validated_data['skills']
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'profile_image', 'resume', 'skills']
    
class AddCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddCompanies
        fields = '__all__'

class AddJobSerializer(serializers.ModelSerializer):
    company = AddCompanySerializer(source='company_name', read_only=True)
    class Meta:
        model = AddJob
        fields = '__all__'


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        new_password = attrs.get("new_password")
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        attrs["user"] = user 
        return attrs

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        
        user.set_password(new_password)
        user.save()
        return user
    

class JobApplicationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    job_details = AddJobSerializer(source='job', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'user', 'job', 'applied_at', 'status', 'user_details', 'job_details']