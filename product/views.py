from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permission import IsAdmin
from rest_framework.authentication import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@api_view(['POST'])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
def product_add(request):
    serializers = ProductAddSerializers(data=request.data)
    serializers.is_valid(raise_exception=True)
    serializers.save(product_manager=request.user)
    return Response({"message": "product add successfully."}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def updata_product(request, id):
    if not request.data:
        return Response({
            "Error": "No Data Provided To Update"
        },status=status.HTTP_400_BAD_REQUEST)
    product = get_object_or_404(Product, id=id, product_manager=request.user)
    serializers = ProductUpdateSerializers(product, data=request.data, partial=True)
    serializers.is_valid(raise_exception=True)
    serializers.save()
    return Response(serializers.data,status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
def delete_product(request, id):
    serializers = get_object_or_404(Product, id=id, product_manager=request.user)
    serializers.delete()
    return Response({"message": "product delete successful"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def all_product(request):
    product = Product.objects.all()
    serializers = ProductAddSerializers(product, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_search(request, name):
    product = Product.objects.filter(name__icontains=name)
    if not product.exists():
        return Response({"message": "product not available"}, status=status.HTTP_400_BAD_REQUEST)
    serializers = ProductAddSerializers(product, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
    

@api_view(["GET"])
def category_search(request, category):
    product_category = Product.objects.filter(category__icontains=category)
    if not product_category.exists():
        return Response({"message": "this product not found"}, status=status.HTTP_400_BAD_REQUEST)
    serializers = ProductAddSerializers(product_category, many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def order_product(request):
    serializer = ProductOrderSerializers(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

