# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import SingleImage
from .serializers import SingleImageSerializer
from .utils.utils import inverse_classes


import numpy as np
# import tensorflow as tf
# import tensorflow.keras as keras
# from tensorflow.keras import backend as k
# from tensorflow.python.keras.backend import set_session
from tensorflow.keras.applications import vgg16
from tensorflow.keras.models import load_model
import os
from django.conf import settings
from django.core.files.storage import default_storage
from tensorflow.keras.preprocessing.image import load_img, img_to_array
# from tensorflow.keras.applications.imagenet_utils import decode_predictions

# Create your views here.


class ListSingleImage(generics.ListCreateAPIView):
  queryset = SingleImage.objects.all()
  serializer_class = SingleImageSerializer


  def post(self, request, *args, **kwargs):

    # label = decode_predictions(predictions)
    # label = str(list(label)[0])

    # print(request.data)
    serializer = SingleImageSerializer(data=request.data)
    if serializer.is_valid():
      res = {}
      singleImage = serializer.save()
      serializer = SingleImageSerializer(singleImage)
      res['sentData'] = serializer.data
      image = request.data['image']
      file_name = "brain.jpg"
      file_name2 = default_storage.save(file_name, image)
      file_url = default_storage.url(file_name2)
      # print(file_url)
      original = load_img(file_url, target_size=(224,224))
      numpy_image = img_to_array(original)
      image_batch = np.expand_dims(numpy_image,axis=0)
      processed_image = vgg16.preprocess_input(image_batch.copy())
      path = os.path.join(settings.MODELS, 'vgg16_model_with_90_acc.h5')
      # with open(path, 'rb') as loaded_model:
      # loaded_model = 
      model = load_model(path)
      predictions = inverse_classes(np.argmax(model.predict(np.reshape(processed_image, (-1,224,224,3))),axis=1))
      # print(predictions)
      res['predictions'] = predictions
      return Response(res, status=status.HTTP_201_CREATED)
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

