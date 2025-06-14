from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Customer
from ..serializers import CustomerSerializer

class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get all customers (Employee only)",
        responses={200: CustomerSerializer(many=True)}
    )
    def get(self, request):
        if request.user.user_type != 'employee':
            return Response({'error': 'Only employees can view customer list'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
