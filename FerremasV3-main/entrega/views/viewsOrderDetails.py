from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Orderdetails
from ..serializers import OrderDetailsSerializer

class OrderDetailsListView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get order details",
        responses={200: OrderDetailsSerializer(many=True)}
    )
    def get(self, request):
        order_details = Orderdetails.objects.all()
        serializer = OrderDetailsSerializer(order_details, many=True)
        return Response(serializer.data)
