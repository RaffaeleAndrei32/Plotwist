from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Rendiamo l'email unica e obbligatoria a livello di database
    email = models.EmailField(unique=True, blank=False)