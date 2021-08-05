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


class Word(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    class Language(models.TextChoices):
        JAPANESE = 'ja'
        ENGLISH = 'en',

    language = models.CharField(
        max_length=2,
        choices=Language.choices
    )

    def __str__(self) -> str:
        return self.name

class Tag(models.Model):
    word_ja = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='tags_ja', blank=True, null=True)
    word_en = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='tags_en', blank=True, null=True)
    synonyms = models.ManyToManyField(Word, related_name='tags_synonyms')

    def __str__(self) -> str:
        name = '名前なし'
        if self.word_ja.name:
            name = self.word_ja.name
        return name

class Node(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='nodes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self) -> str:
        name = '名前なし'
        if self.tag.word_ja.name:
            name = self.tag.word_ja.name
        return name

    class Meta:
        # 同じ親に同じタグを付与することはできない
        constraints = [
            models.UniqueConstraint(
                fields=["tag", "parent"],
                name="tag_unique"
            )
        ]

