import random


def check_pnr_status(pnr):
    """
    Check PNR status (simulated for demo purposes)
    In production, this would integrate with Indian Railways API
    
    Returns: dict with status and other details
    """
    # Simulated PNR statuses
    STATUSES = [
        'CONFIRMED',
        'WAITING LIST',
        'RAC',  # Reservation Against Cancellation
        'GNWL',  # General Waiting List
    ]
    
    # Generate random status for demo
    status = random.choice(STATUSES)
    current_status = status
    berth_details = None
    
    if status == 'CONFIRMED':
        coach = random.choice(['S1', 'S2', 'S3', 'B1', 'B2', 'A1'])
        berth_number = random.randint(1, 72)
        berth_type = random.choice(['Lower', 'Middle', 'Upper', 'Side Lower', 'Side Upper'])
        berth_details = f"{coach}-{berth_number} ({berth_type})"
        current_status = 'CNF'
    elif status == 'WAITING LIST' or status == 'GNWL':
        waiting_number = random.randint(1, 50)
        current_status = f"WL/{waiting_number}"
    elif status == 'RAC':
        rac_number = random.randint(1, 20)
        current_status = f"RAC{rac_number}"
    
    return {
        'pnr': pnr,
        'train_number': f"{random.randint(10000, 29999)}",
        'train_name': random.choice([
            'Rajdhani Express', 'Shatabdi Express', 'Duronto Express', 
            'Mail Express', 'Superfast Express'
        ]),
        'journey_date': '2024-01-15',
        'from_station': random.choice(['New Delhi', 'Mumbai CST', 'Chennai Central', 'Howrah']),
        'to_station': random.choice(['Mumbai CST', 'New Delhi', 'Bangalore City', 'Sealdah']),
        'boarding_point': random.choice(['New Delhi', 'Mumbai CST', 'Chennai Central', 'Howrah']),
        'reservation_upto': random.choice(['Mumbai CST', 'New Delhi', 'Bangalore City', 'Sealdah']),
        'passengers': [
            {
                'passenger_serial': 1,
                'booking_status': current_status,
                'current_status': current_status,
                'coach_position': berth_details
            }
        ],
        'chart_prepared': False,
        'booking_fare': random.randint(500, 3000),
        'ticket_fare': random.randint(500, 3000),
        'quota': random.choice(['GN', 'CK', 'PT'])
    }


def generate_train_pnr():
    """Generate a 10-digit PNR number for train bookings"""
    # Indian Railways PNR format: first digit indicates zone, rest are random
    zone_digit = random.randint(1, 9)
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return str(zone_digit) + remaining_digits
