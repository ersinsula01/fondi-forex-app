# menaxhimi_fondit/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

# Importo pamjet nga simplejwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', RedirectView.as_view(url='/api/fondet/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include('portali_investitorit.urls')),

    # URL-të e reja për autentikim me token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]