from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import decimal

class Fond(models.Model):
    emri = models.CharField(max_length=200, unique=True)
    pershkrimi = models.TextField()
    data_krijimit = models.DateTimeField(auto_now_add=True)
    strategjia = models.TextField(help_text="Përshkrimi i strategjisë së investimit")
    
    vlera_aktuale_e_kuotes = models.DecimalField(
        max_digits=19, 
        decimal_places=4, 
        default=1.0, 
        help_text="Vlera aktuale e tregut për një kuotë të vetme"
    )

    def __str__(self):
        return self.emri

class AsetPortofoli(models.Model):
    fondi = models.ForeignKey(Fond, on_delete=models.CASCADE, related_name='asetet')
    simboli = models.CharField(max_length=20, help_text="P.sh. 'EUR/USD', 'GOLD', 'AAPL'")
    sasia = models.DecimalField(max_digits=19, decimal_places=4)
    vlera_mesatare_blerjes = models.DecimalField(max_digits=19, decimal_places=4)
    data_e_fundit_perditesimit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.simboli} - {self.fondi.emri}"

class VleraNetoeAsetit(models.Model):
    fondi = models.ForeignKey(Fond, on_delete=models.CASCADE, related_name='historia_nav')
    data = models.DateField(unique=True)
    vlera_per_kuote = models.DecimalField(max_digits=19, decimal_places=4)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"NAV për {self.fondi.emri} në {self.data}: {self.vlera_per_kuote}"

class Investim(models.Model):
    investitori = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investimet')
    fondi = models.ForeignKey(Fond, on_delete=models.CASCADE)
    sasia_kuotave = models.DecimalField(max_digits=19, decimal_places=8, default=0.0)
    vlera_totale_investuar = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Investimi i {self.investitori.username} në {self.fondi.emri}"

class Transaksion(models.Model):
    LLOJI_TRANSAKSIONIT = [
        ('DEPOZITE', 'Depozitë'),
        ('TERHEQJE', 'Tërheqje'),
        ('BLERJE', 'Blerje Kuotash'),
        ('SHITJE', 'Shitje Kuotash'),
    ]
    investimi = models.ForeignKey(Investim, on_delete=models.CASCADE, related_name='transaksionet')
    lloji = models.CharField(max_length=10, choices=LLOJI_TRANSAKSIONIT)
    shuma = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(decimal.Decimal('0.01'))])
    sasia_kuotave = models.DecimalField(max_digits=19, decimal_places=8, null=True, blank=True)
    cmimi_per_kuote = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)
    data_transaksionit = models.DateTimeField(auto_now_add=True)
    statusi = models.CharField(max_length=20, default='E Përfunduar')

    def __str__(self):
        return f"{self.lloji} - {self.investimi.investitori.username} - {self.shuma}"

class Dokument(models.Model):
    LLOJI_DOKUMENTIT = [
        ('PROSPEKT', 'Prospekti i Fondit'),
        ('KIID', 'Dokumenti me Informacionin Kyç'),
        ('RAPORT_VJETOR', 'Raport Vjetor'),
        ('RAPORT_GJASHTEMUJOR', 'Raport Gjashtëmujor'),
    ]
    fondi = models.ForeignKey(Fond, on_delete=models.CASCADE, related_name='dokumentet')
    emri_dokumentit = models.CharField(max_length=255)
    lloji = models.CharField(max_length=25, choices=LLOJI_DOKUMENTIT)
    skedari = models.FileField(upload_to='dokumente_fondi/')
    data_publikimit = models.DateField()

    def __str__(self):
        return self.emri_dokumentit