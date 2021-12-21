from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from ..models import Tag

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

