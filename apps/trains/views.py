from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .pnr_service import check_pnr_status, generate_train_pnr
from .models import Train, Station


class PNRStatusView(APIView):
    """API endpoint to check PNR status"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pnr):
        if not pnr or len(pnr) != 10:
            return Response(
                {'error': 'Invalid PNR number. PNR must be 10 digits.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get PNR status
        pnr_data = check_pnr_status(pnr)
        
        return Response(pnr_data)


class GeneratePNREndpoint(APIView):
    """API endpoint to generate a new PNR (for demo/testing)"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        pnr = generate_train_pnr()
        return Response({'pnr': pnr})


class TrainSearchView(APIView):
    """API endpoint to search trains between stations"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        from_station = request.query_params.get('from')
        to_station = request.query_params.get('to')
        journey_date = request.query_params.get('date')
        
        if not from_station or not to_station:
            return Response(
                {'error': 'Source and destination stations are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search trains
        trains = Train.objects.filter(
            source_station__code=from_station.upper(),
            destination_station__code=to_station.upper()
        )
        
        train_data = []
        for train in trains:
            train_data.append({
                'train_number': train.train_number,
                'train_name': train.train_name,
                'train_type': train.train_type,
                'departure_time': str(train.departure_time),
                'arrival_time': str(train.arrival_time),
                'duration': train.duration,
                'available_classes': train.available_classes,
                'source': train.source_station.name,
                'destination': train.destination_station.name,
            })
        
        return Response({'trains': train_data})
