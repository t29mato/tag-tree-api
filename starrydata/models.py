from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=64)
    memo = models.TextField(blank=True, null=True)
    synonyms = models.ManyToManyField("self", blank=True)
    def __str__(self) -> str:
        return self.name

class Node(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

class TagTree(models.Model):
    name = models.CharField(max_length=64, unique=True)
    key = models.CharField(max_length=32, unique=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self) -> str:
        return self.name
