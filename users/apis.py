from django.http import JsonResponse
from rest_framework.decorators import list_route

from .models import User
from .serializers import UserRegistrationSerializer


@list_route(methods=['post'])
def register(request):
    serialized = UserRegistrationSerializer(data=request.data)
    if serialized.is_valid():
        User.objects.create_user(
            serialized.data['email'],
            serialized.data['password']
        )
        return JsonResponse({"status": "200", "message": "OK"})
    else:
        return JsonResponse({"status": "400", "message": serialized.errors})
