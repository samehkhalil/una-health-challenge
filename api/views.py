from .models import Level
from api.serializers import LevelSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from django.conf import settings
import pandas
import os
from rest_framework.exceptions import ValidationError

class LevelList(ListAPIView):
    """ Level List endpoint """

    serializer_class = LevelSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp', 'glucose_value']

    def get_queryset(self):
        """
            Override default implementation to include filters for 
            user_id: required
            start: optional
            stop: optional
        """
        queryset = Level.objects.all()
        user_id = self.request.query_params.get('user_id')

        if user_id is None:
            # user_id is required
            raise ValidationError(detail='User ID required')

        queryset = queryset.filter(user_id=user_id)
        
        start = self.request.query_params.get('start')
        if start is not None:
            queryset = queryset.filter(timestamp__gte=start)

        stop = self.request.query_params.get('stop')
        if stop is not None:
            queryset = queryset.filter(timestamp__lte=stop)

        return queryset

class LevelDetail(RetrieveAPIView):
    """ Level Detail endpoint """
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class LevelDataPrePopulate(APIView):
    """ PrePopulate POST endpoint """
    
    def post(self, request, format=None):
        Level.objects.all().delete()
        users = [
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "cccccccc-cccc-cccc-cccc-cccccccccccc"
        ]
        for user in users:
            filename = os.path.join(settings.BASE_DIR, f'sample-data/{user}.csv')
            data = pandas.read_csv(filename, skiprows=1)
            
            # keep only columns that are of importance to our use case
            columns = ['Gerätezeitstempel', 'Glukosewert-Verlauf mg/dL']
            df = data[columns]
            
            # drop all records containing empty values
            df = df.dropna()

            # correct datetime format
            df[columns[0]] = pandas.to_datetime(df[columns[0]])
            records = []
            for _, row in df.iterrows():
                records.append(
                    Level(
                        user_id=user,
                        timestamp=row[columns[0]],
                        glucose_value=row[columns[1]]
                    )
                )
            Level.objects.bulk_create(records)
            
        return Response(status=status.HTTP_201_CREATED)

