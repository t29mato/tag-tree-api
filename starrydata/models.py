from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

class TagMemo(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    memo = models.TextField()

class Node(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
