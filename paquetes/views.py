from django.shortcuts import render
from rest_framework import generics

from .models import Paquete
from .serializers import PaqueteSerializer

class PaqueteListAPIView(generics.ListAPIView):
	queryset = Paquete.objects.all()
	serializer_class = PaqueteSerializer
