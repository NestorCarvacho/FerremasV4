from rest_framework.views import APIView
from rest_framework.response import Response

class OrderShipperView(APIView):
    def get(self, request):
        return Response({'message': 'OrderShipper endpoint'})
