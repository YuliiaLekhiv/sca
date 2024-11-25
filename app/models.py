from django.db import models
from .validators import validate_breed

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    breed = models.CharField(max_length=50, validators=[validate_breed])
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Mission(models.Model):
    cat = models.OneToOneField(SpyCat, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.id} for {self.cat.name if self.cat else 'Unassigned'}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.complete:
            self.targets.update(complete=True)

class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Unknown')
    notes = models.TextField(blank=True, default='')
    complete = models.BooleanField(default=False)
    breed = models.CharField(max_length=50, validators=[validate_breed], blank=True, default='Unknown')
    mission = models.ForeignKey('Mission', related_name='targets', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
