from django.core.management.base import BaseCommand
from typing import Optional, TypedDict
from starrydata.models import PolymerTag, PolymerTagTreeNode
import json

class Command(BaseCommand):
    Tree = TypedDict('Tree', {'id': str, 'modified': int, 'text': str, 'children': Optional[list['Tree']]})
    help = 'Import Initial Data to Database'

    def handle(self, *args, **options):
        json_open = open('starrydata/management/commands/initial_data/polymer.json', 'r')
        tree = json.load(json_open)
        parents: List['Tree'] = list(map(lambda parent: parent, tree['nodes']))

        root_node = {
            'node_id': 1,
            'name': '高分子'
        }
        root_exist = PolymerTagTreeNode.objects.filter(pk=root_node['node_id']).exists()
        if not root_exist:
            rootTag = PolymerTag(name=root_node['name'])
            rootTag.save()
            rootNode = PolymerTagTreeNode(polymer_tag=rootTag)
            rootNode.save()
            print('ルートノードが存在しないのでルートノードを作成')
        list(map(lambda parent: self.importTree(root_node['node_id'], parent), parents))

    def importTree(self, parent_id: int,tree: Tree):
        print('処理開始：「' + tree['text'] + '」')
        parent = PolymerTagTreeNode.objects.get(pk=parent_id)

        tag = PolymerTag.objects.filter(name=tree['text'])

        if tag.exists():
            node = PolymerTagTreeNode.objects.filter(polymer_tag=tag[0], parent=parent)
            if node.exists():
                print('処理不要：タグもノードも存在するため')
            else:
                newNode = PolymerTagTreeNode(polymer_tag=tag[0],parent=parent)
                newNode.save()
                print('新規ノード生成完了：「' + parent.polymer_tag.name + '」')
        else:
            newTag = PolymerTag(name=tree['text'])
            newTag.save()
            print('新規タグ生成完了：「' + newTag.name + '」')
            newNode = PolymerTagTreeNode(polymer_tag=tag[0],parent=parent)
            newNode.save()
            print('新規ノード生成完了 - 親：「' + parent.polymer_tag.name + '」')
        print('処理終了：「' + tree['text'] + '」\n')

        node = PolymerTagTreeNode.objects.get(polymer_tag=tag[0], parent=parent)
        if 'children' in tree:
            list(map(lambda child: self.importTree(node.pk, child), tree['children']))
            pass

        # parent_idに対して、ノードの作成（重複がなければ）
        # childrenがいる場合、親とともに下のツリーを渡す
        pass
