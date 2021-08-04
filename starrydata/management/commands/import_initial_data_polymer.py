from django.core.management.base import BaseCommand
from typing import Optional, TypedDict
from starrydata.models import Tag, Node, Word
import requests, re, json

class Command(BaseCommand):
    Tree = TypedDict('Tree', {'id': str, 'modified': int, 'text': str, 'children': Optional[list['Tree']]})
    help = 'Import Initial Data to Database'

    def handle(self, *args, **options):
        payload = {'docId': 'nRDcYKPtj-'}
        headers = {
            'Jwt-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJhcHAiOiJ0cmFuc25vIiwic3ViIjoiMTA4MjU0MDkiLCJsb2dpblR5cGUiOiJlbWFpbCIsImV4cCI6MTYyNjU4MzQ2OCwiaWF0IjoxNjIzOTkxNDY4fQ.ErmJOBrQ22yfgpyMgzMNU4OX-IjOGwzMsWlFb_Nu4PfL9A9KNKD0nMP0dStq5reX7e5PcxJrLTxUcKJ4ID1djw',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json'
            }
        r = requests.post('https://api.transno.com/v3/api/document/view/get', data=json.dumps(payload), headers=headers)
        rootName = r.json()['data']['name']
        # transnoのAPIのレスポンスにspanタグが含まれるため除去
        tree = json.loads(re.sub('</?span>','',r.json()['data']['definition']))['nodes']

        rootWord = Word.objects.filter(name=rootName)
        if not rootWord.exists():
            word = Word(name=rootName, language='jp')
            word.save()
            print('ルート単語生成：「' + rootName + '」')

        rootTag = Tag.objects.filter(word_ja__name=rootName)
        if not rootTag.exists():
            tag = Tag(word_ja=rootWord[0])
            tag.save()
            print('ルートタグ生成：「' + rootName + '」')

        rootNode = Node.objects.filter(tag__word_ja=rootWord[0]).values('id')
        if not rootNode.exists():
            node = Node(tag=rootTag[0])
            node.save()
            print('ルートノード生成「' + rootName + '」')

        list(map(lambda parent: self.__importTree(rootNode[0]['id'], parent), tree))

    def __importTree(self, parent_id: int, tree: Tree):
        print('処理開始：「' + tree['text'] + '」')
        parent = Node.objects.get(pk=parent_id)

        tag = Tag.objects.filter(word_ja__name=tree['text'])

        if tree['text'] == '':
            print('処理不要：タグ名が付いていないため')
            pass

        if tag.exists():
            node = Node.objects.filter(tag=tag[0], parent=parent)
            if node.exists():
                print('処理不要：タグもノードも存在するため')
            else:
                newNode = Node(tag=tag[0],parent=parent)
                newNode.save()
                print('新規ノード生成 - 親：「' + parent.tag.word_ja.name + '」')
        else:
            newWord = Word(name=tree['text'], language='jp')
            newWord.save()
            print('新規単語生成：「' + newWord.name + '」')
            newTag = Tag(word_ja=newWord)
            newTag.save()
            print('新規タグ生成：「' + newTag.word_ja.name + '」')
            newNode = Node(tag=tag[0],parent=parent)
            newNode.save()
            print('新規ノード生成 - 親：「' + parent.tag.word_ja.name + '」')
        print('')

        node = Node.objects.get(tag=tag[0], parent=parent)
        if 'children' in tree:
            list(map(lambda child: self.__importTree(node.pk, child), tree['children']))
            pass
