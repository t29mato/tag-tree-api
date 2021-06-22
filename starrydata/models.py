from django.db import models

# Create your models here.
class FabricationProcess(models.Model):
    name_ja = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name_ja
