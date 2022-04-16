from rest_framework import generics, status
from rest_framework.response import Response

from .models import SingleImage
from .serializers import SingleImageSerializer
from .utils.utils import inverse_classes


import numpy as np
from tensorflow.keras.applications import vgg16
from tensorflow.keras.models import load_model
import os
from PIL import Image
import requests
from django.conf import settings
from django.core.files.storage import default_storage
from tensorflow.keras.preprocessing.image import img_to_array


# Create your views here.
def loadImage(URL):
  img = Image.open(requests.get(URL, stream=True).raw)
  img = img.resize((224, 224), Image.LANCZOS)
  return img_to_array(img)

class ListSingleImage(generics.ListCreateAPIView):
  queryset = SingleImage.objects.all()
  serializer_class = SingleImageSerializer


  def post(self, request, *args, **kwargs):
    res = {}
    try:
      image = request.data['image']
      file_name = "brain.jpg"
      file_name2 = default_storage.save(file_name, image)
      file_url = default_storage.url(file_name2)
      numpy_image = loadImage(file_url)
      image_batch = np.expand_dims(numpy_image,axis=0)
      processed_image = vgg16.preprocess_input(image_batch.copy())
      path = os.path.join(settings.MODELS, 'vgg16_model_with_90_acc.h5')
      model = load_model(path)
      predictions = inverse_classes(np.argmax(model.predict(np.reshape(processed_image, (-1,224,224,3))),axis=1))
      res['predictions'] = predictions
    except:
      res['predictions'] = 'Oops... Something went wrong!'

    return Response(res, status=status.HTTP_201_CREATED)


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

