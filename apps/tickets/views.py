from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Flight, Train, Bus
from .serializers import FlightSerializer, TrainSerializer, BusSerializer


class FlightListView(generics.ListCreateAPIView):
    """API endpoint to list and search flights"""
    queryset = Flight.objects.filter(is_cancelled=False)
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source', 'destination', 'journey_date', 'airline_name']
    ordering_fields = ['base_fare', 'departure_time']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(base_fare__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_fare__lte=max_price)
        
        return queryset


class FlightDetailView(generics.RetrieveAPIView):
    """API endpoint to get flight details"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrainListView(generics.ListCreateAPIView):
    """API endpoint to list and search trains"""
    queryset = Train.objects.filter(is_cancelled=False)
    serializer_class = TrainSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source', 'destination', 'journey_date', 'train_name']
    ordering_fields = ['base_fare', 'departure_time']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(base_fare__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_fare__lte=max_price)
        
        return queryset


class TrainDetailView(generics.RetrieveAPIView):
    """API endpoint to get train details"""
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BusListView(generics.ListCreateAPIView):
    """API endpoint to list and search buses"""
    queryset = Bus.objects.filter(is_cancelled=False)
    serializer_class = BusSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source', 'destination', 'journey_date', 'bus_operator']
    ordering_fields = ['base_fare', 'departure_time']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(base_fare__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_fare__lte=max_price)
        
        return queryset


class BusDetailView(generics.RetrieveAPIView):
    """API endpoint to get bus details"""
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
