from django.db import models

# Create your models here.


class Data(models.Model):
    json_data = models.CharField(max_length=10000000)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return "Data: " + str(self.created_at)
