from django.db import models

class Database(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Paper(models.Model):
    title = models.CharField(max_length=1000)
    authors = models.CharField(max_length=1000)
    identifier = models.CharField(max_length=32)
    DOI = models.CharField(max_length=32)
    container_title = models.CharField(max_length=1000, blank=True, null=True)
    publisher = models.CharField(max_length=1000, default='')
    database = models.ManyToManyField(Database)

    def __str__(self) -> str:
        return self.title

class Figure(models.Model):
    title = models.CharField(max_length=100)
    paper = models.ManyToManyField(Paper)

    def __str__(self) -> str:
        return self.title

class Sample(models.Model):
    name = models.CharField(max_length=100)
    paper = models.ManyToManyField(Paper)

    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    name_ja = models.CharField(max_length=255, unique=True)
    name_en = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name_ja

class Node(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='nodes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self) -> str:
        return self.tag.name_ja

    class Meta:
        # 同じ親に同じタグを付与することはできない
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "parent"],
                name="tag_unique"
            )
        ]
