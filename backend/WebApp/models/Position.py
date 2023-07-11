from django.db import models


class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    specific_positions = models.CharField(max_length=100, null=True)

    @classmethod
    def create(cls, name, specific_positions):
        position = Position.objects.create(name=name, specific_positions=specific_positions)
        return position

    def __str__(self):
        return self.name