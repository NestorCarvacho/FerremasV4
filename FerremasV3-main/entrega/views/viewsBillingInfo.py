from rest_framework.views import APIView
from rest_framework.response import Response

class BillingInfoView(APIView):
    def get(self, request):
        return Response({'message': 'BillingInfo endpoint'})
