from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import authenticate 
from django.shortcuts import get_object_or_404
from .serializers import *
from .utils import *
from .models import *
import random


@api_view(['POST'])
def Signup(request):
    serializers = SignupSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    User.objects.create_user(
        username=serializers.validated_data["username"],
        email=serializers.validated_data["email"],
        password=serializers.validated_data["password"],
        role=serializers.validated_data["role"],
        phone=serializers.validated_data["phone"]
    )
    
    return Response({"message": "User Registration Successful."}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def Signin(request):
    serializers = SigninSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    user = authenticate(
        request,
        username=serializers.validated_data["username"],
        password=serializers.validated_data["password"]
    )
    
    if user is not None:
        token = get_tokens_for_user(user)
        return Response({"message": "Login Successfully.", "access_token": token["access"], "refresh_token": token["refresh"]}, status=status.HTTP_200_OK)
    
    return Response({"message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def change_password(request):
    serializers = ChangePasswordSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    user = get_object_or_404(User, id=request.user.id)
    if user.check_password(serializers.validated_data["old_password"]):
        user.set_password(serializers.validated_data["new_password"])
        user.save()
        return Response({"message": "Password Change Successful."}, status=status.HTTP_200_OK)
    
    return Response({"message": "Invalid Old Password"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_otp(request):
    serializers  = CreateOtpSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    username=serializers.validated_data["username"]
    
    
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        
    
        otp = {
            "user": user,
            "otp": random.randint(1000, 9999)
        }
    
        OTP.objects.create(**otp)
    
        return Response({"Status": "Success", "message": "Otp create success"}, status=status.HTTP_201_CREATED)
    
    return Response({"status": "failed", "message": "Email dose not exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["POST"])
def reset_password(request):
    serializers = RestPasswordSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    
    username=serializers.validated_data["username"]
    otp=serializers.validated_data["otp"]
    new_password=serializers.validated_data["new_password"]
    
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        db_otp = OTP.objects.filter(otp=otp).last()
        
        if str(otp) == str(db_otp.otp):
            if not db_otp.is_expired:
                return Response({
                    "status" : "Error",
                    "message": "otp is expired",
                },status=status.HTTP_201_CREATED)
            
            user.set_password(new_password)
            user.save()
            
            return Response({
                "status": "success",
                "message": "password reset successful"
            }, status=status.HTTP_200_OK)
            
        return Response({
            "status": "failed",
            "message": "wrong otp"
        }, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        "status": "failed",
        "message": "username dosenot exists"
    },status=status.HTTP_400_BAD_REQUEST)
