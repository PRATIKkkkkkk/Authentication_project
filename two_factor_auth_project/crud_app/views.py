from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer
from .models import Student
import logging
import datetime
from django.shortcuts import get_object_or_404

logger = logging.getLogger('logger')



class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        objs = Student.objects.all()
        serializer = StudentSerializer(objs, many=True)
        logger.info(f'Get method called at time: {datetime.datetime.now()}') 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Student Added at time: {datetime.datetime.now()}') 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f'False Data provided at: {datetime.datetime.now()}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        obj = get_object_or_404(Student, pk=pk)
        serilaizer = StudentSerializer(obj)
        logger.info(f'Get method called at time: {datetime.datetime.now()}')
        return Response(serilaizer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        obj = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(request.data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Student Updated at time: {datetime.datetime.now()}')
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f'False Data provided While Update at: {datetime.datetime.now()}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, pk):
        obj = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(request.data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'Student Updated at time: {datetime.datetime.now()}')
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f'False Data provided While Update at: {datetime.datetime.now()}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        obj = get_object_or_404(Student, pk=pk)
        obj.delete()
        logger.info(f'Student Deleted at time: {datetime.datetime.now()}')
        return Response(status=status.HTTP_204_NO_CONTENT)
