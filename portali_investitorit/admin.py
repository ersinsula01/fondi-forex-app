# portali_investitorit/admin.py

from django.contrib import admin
from .models import Fond, AsetPortofoli, VleraNetoeAsetit, Investim, Transaksion, Dokument

# Regjistron çdo model në panelin e adminit
admin.site.register(Fond)
admin.site.register(AsetPortofoli)
admin.site.register(VleraNetoeAsetit)
admin.site.register(Investim)
admin.site.register(Transaksion)
admin.site.register(Dokument)