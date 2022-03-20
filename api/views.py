from .models import Level
from api.serializers import LevelSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import filters

class LevelList(ListAPIView):
    serializer_class = LevelSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp', 'glucose_value']
    # TODO
    # check sorting

    # raise error if user param does not exist
    # raise error if data no valid format
    def get_queryset(self):
        """
            Override default implementation to include filters for 
            user_id: required
            start: optional
            stop: optional
        """
        queryset = Level.objects.all()
        user_id = self.request.query_params.get('user_id')
        start = self.request.query_params.get('start')
        stop = self.request.query_params.get('stop')

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        
        if start is not None:
            queryset = queryset.filter(timestamp__gte=start)
        
        if stop is not None:
            queryset = queryset.filter(timestamp__lte=stop)

        return queryset

class LevelDetail(RetrieveAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
