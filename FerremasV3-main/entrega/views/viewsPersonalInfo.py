from rest_framework.views import APIView
from rest_framework.response import Response

class PersonalInfoView(APIView):
    def get(self, request):
        return Response({'message': 'Personal Info endpoint'})
