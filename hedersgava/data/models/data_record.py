"""Data record"""
from django.db import models
from . import data_set, device


class DataRecord(models.Model):
    """Data record model"""
    value = models.DecimalField(max_digits=10, decimal_places=5)
    datetime = models.DateTimeField()
    data_set = models.ForeignKey(data_set.DataSet, on_delete=models.CASCADE)
    device = models.ForeignKey(device.Device, on_delete=models.CASCADE)

    class Meta:
        ordering = ('datetime',)
        indexes = [
            models.Index(fields=('datetime',))
        ]
