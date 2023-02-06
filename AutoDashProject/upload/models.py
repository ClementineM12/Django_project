from django.db import models

# Create your models here.
class Data(models.Model):
    description = models.CharField(max_length=50, blank=True)
    document = models.FileField(upload_to='documents/')
    time_stamp = models.DateTimeField(auto_now_add=True)
    # TODO later on User_ID 
