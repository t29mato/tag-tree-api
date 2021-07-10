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

class PolymerTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class PolymerTagTreeNode(models.Model):
    polymer_tag = models.ForeignKey(PolymerTag, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self) -> str:
        return self.polymer_tag.name


class FabricationProcess(models.Model):
    name_ja = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name_ja

class SynthesisMethodTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id) + ': ' + self.name

class SynthesisMethodTagTreeNode(models.Model):
    name = models.CharField(max_length=100)
    synthesis_method_tag = models.ForeignKey(SynthesisMethodTag, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id) + ': ' + self.name
