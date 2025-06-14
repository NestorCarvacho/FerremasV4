from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Shipper
from ..serializers import ShipperSerializer

class ShipperListView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get all shippers",
        responses={200: ShipperSerializer(many=True)}
    )
    def get(self, request):
        shippers = Shipper.objects.all()
        serializer = ShipperSerializer(shippers, many=True)
        return Response(serializer.data)
