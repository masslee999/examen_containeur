from django.db import models
from django.core.validators import EmailValidator

# Create your models here.
class DevStudents(models.Model):
    STATUT_CHOICES = [('Actif', 'Actif'),
                      ('Non Actif', 'Non Actif'),]

    fname = models.CharField(max_length=50, verbose_name='Noms')
    sname = models.CharField(max_length=50, verbose_name='Prénoms')
    email = models.CharField(max_length=100, unique=True, validators=[EmailValidator()], verbose_name="Email")
    mot_de_passe = models.CharField(max_length=255, verbose_name="Mot de passe")
    active = models.CharField(max_length=10, choices=STATUT_CHOICES, default='Actif', verbose_name='Statut')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Etudiant dévéloppeur"
        verbose_name_plural = "Etudiants dévéloppeurs"
        db_table = "DevStudents"

    def __str__(self):
        return f" {self.sname} {self.fname}"