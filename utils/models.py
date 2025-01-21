from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nominal = models.IntegerField(null=True, blank=True)
    lifetime = models.IntegerField(null=True, blank=True)
    restock = models.IntegerField(null=True, blank=True)
    min = models.IntegerField(null=True, blank=True)
    quantmin = models.IntegerField(null=True, blank=True)
    quantmax = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    tier = models.CharField(max_length=255, null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
