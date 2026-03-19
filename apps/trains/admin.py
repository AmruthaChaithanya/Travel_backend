from django.contrib import admin
from .models import Station, Train

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'state']
    search_fields = ['name', 'code']
    list_filter = ['state']


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ['train_number', 'train_name', 'train_type', 'source_station', 'destination_station', 'duration']
    list_filter = ['train_type']
    search_fields = ['train_number', 'train_name']
