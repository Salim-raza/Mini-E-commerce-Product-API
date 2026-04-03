from django.contrib.auth.models import User
from rest_framework import serializers


class SignupSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "phone", "role"]

class SigninSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    
class RestPasswordSerializers(serializers.Serializer):
    email =  serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()

class CreateOtpSerializers(serializers.Serializer):
    username = serializers.CharField()
