from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Fond, Investim, Transaksion
from .serializers import (
    FondListSerializer, 
    FondDetailSerializer, 
    InvestimSerializer,
    UserCreateSerializer,
    InvestoSerializer,
    MyTokenObtainPairSerializer
)

# Pamje e personalizuar për marrjen e token-it
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Pamje për të listuar të gjitha fondet (publike)
class FondListAPIView(generics.ListAPIView):
    queryset = Fond.objects.all()
    serializer_class = FondListSerializer
    permission_classes = [permissions.AllowAny]

# Pamje për të parë detajet e një fondi specifik (publike)
class FondDetailAPIView(generics.RetrieveAPIView):
    queryset = Fond.objects.all()
    serializer_class = FondDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

# Pamje për të parë investimet personale (kërkon login)
class MyInvestmentsAPIView(generics.ListAPIView):
    serializer_class = InvestimSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Investim.objects.filter(investitori=self.request.user)

# Pamje për të regjistruar një përdorues të ri (publike)
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

# Pamje për të kryer një investim (kërkon login)
class InvestoAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        fond_id = serializer.validated_data['fond_id']
        shuma = serializer.validated_data['shuma']
        investitori = request.user
        
        fondi = get_object_or_404(Fond, id=fond_id)
        
        investimi, created = Investim.objects.get_or_create(
            investitori=investitori,
            fondi=fondi
        )
        
        investimi.vlera_totale_investuar += shuma
        investimi.sasia_kuotave += shuma 
        investimi.save()
        
        Transaksion.objects.create(
            investimi=investimi,
            lloji='BLERJE',
            shuma=shuma,
            sasia_kuotave=shuma,
            statusi='E Përfunduar'
        )
        
        return Response(
            {"mesazhi": f"Investimi prej {shuma} EUR në fondin '{fondi.emri}' u krye me sukses."},
            status=status.HTTP_201_CREATED
        )