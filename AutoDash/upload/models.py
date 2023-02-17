from django.db import models

# Create your models here.

class Data(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.CharField(max_length=250)
    time_stamp = models.DateTimeField(auto_now_add=True)
    # TODO later on User_ID 