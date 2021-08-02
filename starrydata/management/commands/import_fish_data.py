from django.core.management.base import BaseCommand
from starrydata.models import Tag, Node, Word
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_file = open("starrydata/management/commands/fish-tree.csv", "r", encoding="UTF-8", errors="", newline="")
        f = csv.DictReader(csv_file, delimiter=",", doublequote=False, lineterminator="\r\n", quotechar="'", skipinitialspace=True)
        for row in f:
            words = Word.objects.filter(name=row["category_name"])
            if not words.exists():
                word = Word(name=row["category_name"], language=Word.Language.JAPANESE)
                word.save()
                print('単語追加：「' + row["category_name"] + '」')
            else:
                print('単語追加なし：「' + row["category_name"] + '」')

            tags = Tag.objects.filter(word_ja__name=row["category_name"])
            if not tags.exists():
                tag = Tag(word_ja=words[0])
                tag.save()
                print('タグ追加：「' + row["category_name"] + '」')
            else:
                print('タグ追加なし：「' + row["category_name"] + '」')


            nodes = Node.objects.filter(tag__word_ja=words[0])
            if not nodes.exists():
                if row["parent_id"] == '0':
                    rootNode = Node(tag=tags[0], id=row["id"], parent=None)
                    rootNode.save()
                    print('ルートノード追加：「' + row["category_name"] + '」')
                    continue
                parent = Node.objects.get(id=row["parent_id"])
                node = Node(tag=tags[0], id=row["id"], parent=parent)
                node.save()
                print('ノード追加：「' + row["category_name"] + '」')
            else:
                print('ノード追加なし：「' + row["category_name"] + '」')
            print()
