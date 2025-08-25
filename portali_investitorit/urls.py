from django.urls import path
from .views import (
    FondListAPIView, 
    FondDetailAPIView, 
    MyInvestmentsAPIView,
    UserCreateAPIView,
    InvestoAPIView
)

urlpatterns = [
    path('regjistrohu/', UserCreateAPIView.as_view(), name='regjistrohu'),
    path('investo/', InvestoAPIView.as_view(), name='investo'),
    path('fondet/', FondListAPIView.as_view(), name='lista-e-fondeve'),
    path('fondet/<int:pk>/', FondDetailAPIView.as_view(), name='detajet-e-fondit'),
    path('investimet-e-mia/', MyInvestmentsAPIView.as_view(), name='investimet-e-mia'),
]