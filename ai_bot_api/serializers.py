from rest_framework import serializers
from .models import CustomUser,AddCompanies
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number', 'profile_image']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            profile_image=validated_data.get('profile_image')
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'profile_image']
    
class AddCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddCompanies
        fields = '__all__'


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        current_password = attrs.get("current_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

     
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

       
        if not user.check_password(current_password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

      
        if new_password != confirm_password:
            raise serializers.ValidationError({"new_password": "New passwords do not match."})

        attrs["user"] = user 
        return attrs

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user