from django.db import models

class Nation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image_path = models.CharField(max_length=250, null=True)

    @classmethod
    def create(cls, name, image):
        nation = Nation.objects.create(name=name, image_path=image)
        return nation

    def __str__(self):
        return self.name