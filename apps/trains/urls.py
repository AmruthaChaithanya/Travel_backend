from django.urls import path
from .views import (
    PNRStatusView,
    GeneratePNREndpoint,
    TrainSearchView,
)

urlpatterns = [
    path('pnr/<str:pnr>/', PNRStatusView.as_view(), name='pnr-status'),
    path('generate-pnr/', GeneratePNREndpoint.as_view(), name='generate-pnr'),
    path('search/', TrainSearchView.as_view(), name='train-search'),
]
