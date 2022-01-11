from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from ..models import Tag, TagTree
import uuid

class TestTagCreateAPIView(APITestCase):
    TARGET_URL = '/api/tags'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user',
            email='user@example.com',
            password='secret',
        )

    def test_create_success(self):
        params = {
            "data": {
                "type": "Tag",
                "attributes": {
                    "name": "fish",
                    "memo": "beautiful fish"
                }
            }
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.TARGET_URL, params)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 1)
        tag = Tag.objects.get()
        expected = {
            "data": {
                "type": "Tag",
                "id": str(tag.id),
                "attributes": {
                    "name": tag.name,
                    "memo": tag.memo
                }
            }
        }
        self.assertJSONEqual(
            raw=response.content,
            expected_data=expected
        )

class TestTagTreeCreateAPIView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user',
            email='user@example.com',
            password='secret',
        )


    def test_create_success(self):
        TARGET_URL = '/api/tag_tree'
        KEY = uuid.uuid1().hex
        PARAMS = {
            "data": {
                "type": "TagTreeListView",
                "attributes": {
                    "name": KEY,
                    "key": KEY,
                }
            }
        }

        self.client.force_authenticate(self.user)
        response = self.client.post(TARGET_URL, PARAMS)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TagTree.objects.count(), 1)
        expected = {
            "data": {
                "type": PARAMS["data"]["type"],
                "id": str(TagTree.objects.get(key=PARAMS["data"]["attributes"]["key"]).pk),
                "attributes": PARAMS["data"]["attributes"]
            }
        }
        self.assertJSONEqual(
            raw=response.content,
            expected_data=expected
        )

    def test_create_tree_success(self):
        KEY = uuid.uuid1().hex
        POST_PARAMS = {
            "data": {
                "type": "TagTreeListView",
                "attributes": {
                    "name": KEY,
                    "key": KEY,
                }
            }
        }

        self.client.force_authenticate(self.user)
        self.client.post('/api/tag_tree', POST_PARAMS)
        ID = str(TagTree.objects.get(key=KEY).pk)

        PATCH_PARAMS = {
            "data": {
                "type": "TagTreeDetailView",
                "id": ID,
                "attributes": {
                    "name": KEY,
                    "key": KEY,
                    "tree": {
                        "tag_name": "parent",
                        "children": [],
                    }
                }
            }
        }
        patchResponse = self.client.patch('/api/tag_tree/'+ID, PATCH_PARAMS)
        self.assertEqual(patchResponse.status_code, 200)

        expected = {
            "data": {
                "type": PATCH_PARAMS["data"]["type"],
                "id": None,
                "attributes": PATCH_PARAMS["data"]["attributes"]
            }
        }
        self.assertJSONEqual(
            raw=patchResponse.content,
            expected_data=expected
        )

        getResponse = self.client.get('/api/tag_tree/'+ID)
        self.assertEqual(getResponse.status_code, 200)

        expected = {
            "data": {
                "type": PATCH_PARAMS["data"]["type"],
                "id": None,
                "attributes": {
                    "name": KEY,
                    "key": KEY,
                    "tree": {
                        "tag_name": "parent",
                        "children": [],
                        "tree_level": 0,
                    }
                }
            }
        }
        self.assertJSONEqual(
            raw=getResponse.content,
            expected_data=expected
        )
