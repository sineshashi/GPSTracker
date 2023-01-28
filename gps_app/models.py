from tortoise.models import Model
from tortoise import fields

class DeviceGPSInfoTable(Model):
    id = fields.IntField(pk=True)
    device_id = fields.IntField(index=True)
    latitude = fields.FloatField(null=False)
    longitude = fields.FloatField(null=False)
    timestamp = fields.DatetimeField(index=True)
    sts = fields.DatetimeField(null=False)
    speed = fields.FloatField(null=False)