from django.db import models
import uuid

class Level(models.Model):
    """ Represents a Glucose Level Reading """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.UUIDField()
    timestamp = models.DateTimeField()
    glucose_value = models.IntegerField()