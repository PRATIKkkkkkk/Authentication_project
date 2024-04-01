from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .seializers import User, UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import jwt


class UserAPI(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.is_active = False
            obj.save()
            current_site = get_current_site(request).domain
            relative_link = reverse('verify_email')

            subject = 'Verify Email'
            email = request.data.get('email')

            token = RefreshToken.for_user(obj).access_token
            username = request.data.get('username')

            absolute_url = f'http://{current_site}{relative_link}?token={token}'

            message = f'Hey {username}!!! Click Thin link to verify email \n {absolute_url}'
            send_mail(
                subject=subject,
                recipient_list=[email],
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                fail_silently=False,
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Veriy_Email(APIView):

    def get(self, request):
        token = request.GET.get('token')
        # print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            user.is_active = True
            user.save()
            return Response(data={'email': 'Succesfully activated'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifire:
            return Response(data={'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifire:
            return Response(data={'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
