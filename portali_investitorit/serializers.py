from rest_framework import serializers
from .models import Fond, Investim, Transaksion, VleraNetoeAsetit, Dokument
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class TransaksionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaksion
        fields = ['lloji', 'shuma', 'data_transaksionit', 'statusi']

class InvestimSerializer(serializers.ModelSerializer):
    fondi = serializers.StringRelatedField()
    transaksionet = TransaksionSerializer(many=True, read_only=True)
    vlera_aktuale = serializers.SerializerMethodField()
    fitimi = serializers.SerializerMethodField()

    class Meta:
        model = Investim
        fields = ['id', 'fondi', 'sasia_kuotave', 'vlera_totale_investuar', 'vlera_aktuale', 'fitimi', 'transaksionet']

    def get_vlera_aktuale(self, obj):
        vlera = obj.sasia_kuotave * obj.fondi.vlera_aktuale_e_kuotes
        return round(vlera, 2)

    def get_fitimi(self, obj):
        vlera_aktuale = self.get_vlera_aktuale(obj)
        fitimi = vlera_aktuale - obj.vlera_totale_investuar
        return round(fitimi, 2)

class VleraNetoeAsetitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VleraNetoeAsetit
        fields = ['data', 'vlera_per_kuote']

class DokumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dokument
        fields = ['emri_dokumentit', 'lloji', 'skedari', 'data_publikimit']

class FondDetailSerializer(serializers.ModelSerializer):
    historia_nav = VleraNetoeAsetitSerializer(many=True, read_only=True)
    dokumentet = DokumentSerializer(many=True, read_only=True)
    class Meta:
        model = Fond
        fields = ['id', 'emri', 'pershkrimi', 'strategjia', 'data_krijimit', 'historia_nav', 'dokumentet']

class FondListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fond
        fields = ['id', 'emri', 'pershkrimi']

class InvestoSerializer(serializers.Serializer):
    fond_id = serializers.IntegerField()
    shuma = serializers.DecimalField(max_digits=19, decimal_places=2)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token