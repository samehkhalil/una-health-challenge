from django.db import models
import uuid

# Create your models here.
class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,)
    user_id = models.UUIDField()
    timestamp = models.DateTimeField()
    glucose_value = models.IntegerField()