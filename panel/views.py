from .models import Record
from .serializers import RecordSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import json
from django.conf import settings
import urllib.request
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class WeatherList(generics.GenericAPIView):

    serializer_class = RecordSerializer
    
    def get(self, request, *args, **kwargs):

        city = self.kwargs['city']
        if city in cache:
            city = cache.get(city)
            return Response(city, status=status.HTTP_201_CREATED)

        elif city in Record.objects.filter(city=city):
            products = Record.objects.filter(city=city)
            results = [product.to_json() for product in products]
            cache.set(city, results, timeout=CACHE_TTL)
            return Response(results, status=status.HTTP_201_CREATED)

        else:
            source = urllib.request.urlopen(
                'http://api.openweathermap.org/data/2.5/weather?q='
                + city + '&appid=5f1dc89113b691d9e69658562ccb2834').read()

            list_of_data = json.loads(source)

            datas = {
                "city": city,
                "temperature": str(list_of_data['main']['temp']) + 'k',
                "pressure": str(list_of_data['main']['pressure']) + 'hPa',
                "humidity": str(list_of_data['main']['humidity']) + '%',
            }

            temp = str(list_of_data['main']['temp']) + 'k'
            pre = str(list_of_data['main']['pressure']) + 'hPa'
            hum = str(list_of_data['main']['humidity']) + '%'
            Record.objects.create(
                city=city, temperature=temp, pressure=pre, humidity=hum)
            cache.set(city, datas, timeout=CACHE_TTL)
            return Response(status=status.HTTP_201_CREATED, data=datas)
