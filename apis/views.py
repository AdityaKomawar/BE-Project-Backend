from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import SingleImage
from .serializers import SingleImageSerializer

# Create your views here.


class ListSingleImage(generics.ListCreateAPIView):
  queryset = SingleImage.objects.all()
  serializer_class = SingleImageSerializer

  def post(self, request, *args, **kwargs):
    # image = request
    print(request.data)
    serializer = SingleImageSerializer(data=request.data)
    if serializer.is_valid():
      singleImage = serializer.save()
      serializer = SingleImageSerializer(singleImage)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response()


class DetailSingleImage(generics.RetrieveUpdateDestroyAPIView):
  queryset = SingleImage.objects.all()
  serializer_class = SingleImageSerializer

# @csrf_exempt
# def ListSingleImage(request):
#   if request.method == 'GET':
#     singleImage = SingleImage.objects.all()
#     serializer = SingleImageSerializer(singleImage, many=True)
#     return JsonResponse(serializer.data, safe=False)

#   elif request.method == 'POST':
#     data = JSONParser().parse(request)
#     serializer = SingleImageSerializer(data=data)
#     if serializer.is_valid():
#       serializer.save()
#       return JsonResponse(serializer.data, status=201)
#     return JsonResponse(serializer.errors, status=400)

  
# @csrf_exempt
# def DetailSingleImage(request, pk):
#   try:
#     singleImage = SingleImage.objects.get(pk=pk)
#   except SingleImage.DoesNotExist:
#     return HttpResponse(status=400)

#   if request.method == 'GET':
#     serializer = SingleImageSerializer(singleImage)
#     return JsonResponse(serializer.data)

#   elif request.method == 'PUT':
#     data = JSONParser().parse(request)
#     serializer = SingleImageSerializer(singleImage, data=data)

#     if serializer.is_valid():
#       serializer.save()
#       return JsonResponse(serializer.data)
#     return JsonResponse(serializer.errors, status=400)

#   elif request.method == 'DELETE':
#     singleImage.delete()
#     return HttpResponse(status=204)