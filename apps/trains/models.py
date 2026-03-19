from django.db import models


class Station(models.Model):
    """Railway Station model"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)  # Station code (e.g., NDLS, CSTM)
    state = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Train(models.Model):
    """Train model with route information"""
    TRAIN_TYPE = (
        ('EXPRESS', 'Express'),
        ('SUPERFAST', 'Superfast'),
        ('PASSENGER', 'Passenger'),
        ('RAJDHANI', 'Rajdhani'),
        ('SHATABDI', 'Shatabdi'),
        ('DURONTO', 'Duronto'),
    )
    
    COACH_CLASS = (
        ('SL', 'Sleeper'),
        ('3A', 'AC 3 Tier'),
        ('2A', 'AC 2 Tier'),
        ('1A', 'AC First Class'),
        ('CC', 'Chair Car'),
        ('2S', 'Second Sitting'),
    )
    
    train_number = models.CharField(max_length=20, unique=True)
    train_name = models.CharField(max_length=100)
    train_type = models.CharField(max_length=20, choices=TRAIN_TYPE)
    
    # Route info
    source_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source_trains')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_trains')
    
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=20)  # e.g., "12h 30m"
    
    # Availability
    available_classes = models.JSONField(default=list)  # List of available coach classes
    runs_on = models.JSONField(default=dict)  # Days of operation {'mon': True, 'tue': True, ...}
    
    class Meta:
        ordering = ['train_number']
    
    def __str__(self):
        return f"{self.train_number} - {self.train_name}"
