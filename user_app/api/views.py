from rest_framework.decorators import api_view
from user_app.api.serializers import RegSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from user_app import models



@api_view(['POST',])
def logout(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
""" 
we can also create token using 
token = Token.objects.get_or_create(user=account).key
"""

@api_view(['POST',])
def registration_view(request):
    data = {}
    if request.method=='POST':
        serializer = RegSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user=account).key
            data ['username']=account.username
            data['email']=account.email
            data['response']="Registration successsful"
            data['token']=token        
        else:
            data = serializer.errors

        return Response(data)

