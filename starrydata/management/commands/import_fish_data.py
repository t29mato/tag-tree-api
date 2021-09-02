from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection
from starrydata.models import Tag, Node, Term
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_file = open("starrydata/management/commands/fish-tree.csv", "r", encoding="UTF-8", errors="", newline="")
        f = csv.DictReader(csv_file, delimiter=",", doublequote=False, lineterminator="\r\n", quotechar="'", skipinitialspace=True)
        for index, row in enumerate(f):
            print(str(index) + '：' + row["category_name"])
            terms = Term.objects.filter(name=row["category_name"])
            if not terms.exists():
                term = Term(name=row["category_name"], language=Term.Language.JAPANESE)
                term.save()
                print('単語追加')
            else:
                print('単語追加なし')

            tags = Tag.objects.filter(term_ja__name=row["category_name"])
            if not tags.exists():
                tag = Tag(term_ja=terms[0])
                tag.save()
                print('タグ追加')
            else:
                print('タグ追加なし')


            nodes = Node.objects.filter(tag__term_ja=terms[0])
            if not nodes.exists():
                if row["parent_id"] == '0':
                    rootNode = Node(tag=tags[0], id=row["id"], parent=None)
                    rootNode.save()
                    print('ルートノード追加')
                    continue
                parent = Node.objects.get(id=row["parent_id"])
                node = Node(tag=tags[0], id=row["id"], parent=parent)
                node.save()
                print('ノード追加')
            else:
                print('ノード追加なし')
            print()

        print('node tableのsequenceのresetを開始')
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Node])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
        print('node tableのsequenceのresetを終了')
