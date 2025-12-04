from django.db import models

# Create your models here.
class ConfigKeys(models.Model):
    id = models.AutoField(primary_key=True)
    keys = models.CharField(max_length=255, blank=False, null=False)
    values = models.CharField(max_length=255, blank=False, null=False)
    identifier = models.CharField(max_length=100, blank=False, null=False)
    short_codes= models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(default=2025,blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    

    def __str__(self):
        return self.keys

    class Meta: 
        db_table = 'config_keys'