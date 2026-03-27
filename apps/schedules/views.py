from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from datetime import datetime, timedelta
from .models import FlightSchedule, TrainSchedule, BusSchedule
from .serializers import FlightScheduleSerializer, TrainScheduleSerializer, BusScheduleSerializer


def _is_bookable_schedule(schedule, cutoff_hours=6):
    """Return True only when departure is strictly after now + cutoff."""
    departure_at = datetime.combine(schedule.journey_date, schedule.departure_time)
    if timezone.is_naive(departure_at):
        departure_at = timezone.make_aware(departure_at)
    return departure_at > (timezone.now() + timedelta(hours=cutoff_hours))


class FlightScheduleListView(generics.ListAPIView):
    """API endpoint to search and list available flight schedules"""
    serializer_class = FlightScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['departure_airport', 'arrival_airport', 'journey_date', 'airline_name', 'seat_class']
    ordering_fields = ['base_fare', 'departure_time']
    
    def get_queryset(self):
        queryset = FlightSchedule.objects.filter(
            is_active=True,
            is_cancelled=False,
            available_seats__gt=0
        )
        
        # Filter by date range
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        
        if from_date:
            queryset = queryset.filter(journey_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(journey_date__lte=to_date)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(base_fare__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_fare__lte=max_price)
        
        allowed_ids = [schedule.id for schedule in queryset if _is_bookable_schedule(schedule)]
        return queryset.filter(id__in=allowed_ids)


class FlightScheduleDetailView(generics.RetrieveAPIView):
    """API endpoint to get detailed flight schedule information"""
    queryset = FlightSchedule.objects.filter(is_active=True, is_cancelled=False)
    serializer_class = FlightScheduleSerializer
    permission_classes = [permissions.AllowAny]


class TrainScheduleListView(generics.ListAPIView):
    """API endpoint to search and list available train schedules"""
    serializer_class = TrainScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['source_station', 'destination_station', 'journey_date', 'train_type', 'coach_class']
    ordering_fields = ['base_fare', 'departure_time']
    
    def get_queryset(self):
        queryset = TrainSchedule.objects.filter(
            is_active=True,
            is_cancelled=False,
            available_seats__gt=0
        )
        
        # Filter by date range
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        
        if from_date:
            queryset = queryset.filter(journey_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(journey_date__lte=to_date)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(base_fare__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_fare__lte=max_price)
        
        allowed_ids = [schedule.id for schedule in queryset if _is_bookable_schedule(schedule)]
        return queryset.filter(id__in=allowed_ids)


class TrainScheduleDetailView(generics.RetrieveAPIView):
    """API endpoint to get detailed train schedule information"""
    queryset = TrainSchedule.objects.filter(is_active=True, is_cancelled=False)
    serializer_class = TrainScheduleSerializer
    permission_classes = [permissions.AllowAny]


class BusScheduleListView(generics.ListAPIView):
    """API endpoint to search and list available bus schedules"""
    serializer_class = BusScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['boarding_point', 'dropping_point', 'journey_date', 'bus_operator', 'bus_type']
    ordering_fields = ['base_fare', 'departure_time']
    
    def get_queryset(self):
        queryset = BusSchedule.objects.filter(
            is_active=True,
            is_cancelled=False,
            available_seats__gt=0
        )
        
        # Filter by date range
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        
        if from_date:
            queryset = queryset.filter(journey_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(journey_date__lte=to_date)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(base_fare__gte=min_price)
        if max_price:
            queryset = queryset.filter(base_fare__lte=max_price)
        
        allowed_ids = [schedule.id for schedule in queryset if _is_bookable_schedule(schedule)]
        return queryset.filter(id__in=allowed_ids)


class BusScheduleDetailView(generics.RetrieveAPIView):
    """API endpoint to get detailed bus schedule information"""
    queryset = BusSchedule.objects.filter(is_active=True, is_cancelled=False)
    serializer_class = BusScheduleSerializer
    permission_classes = [permissions.AllowAny]


class CheckAvailabilityView(APIView):
    """API endpoint to check seat availability for a schedule"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, schedule_type, pk):
        try:
            if schedule_type == 'flight':
                schedule = FlightSchedule.objects.get(pk=pk)
            elif schedule_type == 'train':
                schedule = TrainSchedule.objects.get(pk=pk)
            elif schedule_type == 'bus':
                schedule = BusSchedule.objects.get(pk=pk)
            else:
                return Response(
                    {'error': 'Invalid schedule type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({
                'schedule_id': schedule.id,
                'schedule_type': schedule_type,
                'available_seats': schedule.available_seats,
                'total_seats': schedule.total_seats,
                'is_available': schedule.available_seats > 0,
                'base_fare': str(schedule.base_fare),
                'total_fare': str(float(schedule.base_fare) + float(schedule.taxes))
            })
        except Exception as e:
            return Response(
                {'error': f'Schedule not found: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )
