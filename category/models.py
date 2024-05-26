import math
from django.db import models
from django.db.models import QuerySet


class Category(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class CategoryMPTT(models.Model):
    name = models.CharField(max_length=20)
    lft = models.IntegerField(default=1)
    rgt = models.IntegerField(default=2)

    class Meta:
        db_table = 'categorymptt'

    def __str__(self):
        return self.name

    @property
    def size(self):
        return math.floor((self.rgt - self.lft + 1) / 2)

    @property
    def is_leaf(self):
        return self.rgt == self.lft + 1

    @property
    def paths(self):
        return (CategoryMPTT.objects.only('name').filter(lft__lte=self.lft, rgt__gte=self.rgt).
                order_by('lft').values_list('name', flat=True))

    def get_children(self) -> QuerySet[Category]:
        return Category.objects.filter(parent=self)

