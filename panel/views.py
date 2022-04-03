from .models import Record
from .serializers import RecordSerializer
from rest_framework.response import Response
from rest_framework import status, generics
import json
from datetime import datetime
from django.conf import settings
import urllib.request
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class WeatherList(generics.GenericAPIView):

    serializer_class = RecordSerializer
    
    def get(self, request, *args, **kwargs):

        citys = self.kwargs['city']
        if citys in cache:
            city = cache.get(citys)
            return Response(city, status=status.HTTP_201_CREATED)

        elif citys in Record.objects.filter(city=citys).values_list('city', flat=True):
            products = Record.objects.filter(city=citys).values('city', 'temperature', 'humidity', 'pressure', 'created')
            results = list(products)
            cache.set(citys, results, timeout=CACHE_TTL)
            return Response(results, status=status.HTTP_201_CREATED)

        else:
            source = urllib.request.urlopen(
                'http://api.openweathermap.org/data/2.5/weather?q='
                + citys + '&appid=5f1dc89113b691d9e69658562ccb2834').read()

            list_of_data = json.loads(source)
            now = datetime.now()
            datas = {
                "city": citys,
                "temperature": str(list_of_data['main']['temp']) + 'k',
                "pressure": str(list_of_data['main']['pressure']) + 'hPa',
                "humidity": str(list_of_data['main']['humidity']) + '%',
                "created": str(now)
            }

            temp = str(list_of_data['main']['temp']) + 'k'
            pre = str(list_of_data['main']['pressure']) + 'hPa'
            hum = str(list_of_data['main']['humidity']) + '%'
            cre = str(now)
            Record.objects.create(
                city=citys, temperature=temp, pressure=pre, humidity=hum, created=cre)
            cache.set(citys, datas, timeout=CACHE_TTL)
            return Response(status=status.HTTP_201_CREATED, data=datas)
