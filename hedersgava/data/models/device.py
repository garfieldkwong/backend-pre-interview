"""Device"""
from django.db import models
UNIT_MAP = {
    'Temperature Sensor': '°C',
    'Voltage Meter': 'V',
    'Current Meter': 'A',
    'Power Meter': 'Wh',
}


class Device(models.Model):
    """Device model"""
    type = models.CharField(max_length=30)
    device_id = models.CharField(max_length=30, unique=True)
    unit = models.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        """Init"""
        if 'type' in kwargs:
            type = kwargs['type']
            kwargs['unit'] = UNIT_MAP[type]
        super().__init__(*args, **kwargs)
