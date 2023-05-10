from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from users.serializers import UserModelSerializer


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='testpassword'
        )

    def test_user_list(self):
        client = APIClient()
        response = client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [UserModelSerializer(self.user).data])

    def test_user_detail(self):
        client = APIClient()
        response = client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client.force_authenticate(user=self.user)
        response = client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'No status')
        friend = User.objects.create_user(username='test_friend', password='testpassword')
        self.user.friends.add(friend)
        response = client.get(f'/api/users/{friend.id}/')
        self.assertEqual(response.data['message'], 'Friends')

    def test_friends_view_set(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/api/friends/', {'user_id': self.user.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'it is impossible to subscribe to yourself'})
        friend = User.objects.create_user(username='test_friend', password='testpassword')
        response = client.post('/api/friends/', {'user_id': friend.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Subscription')
        self.assertTrue(friend in self.user.get_requests())
        response = client.delete(f'/api/friends/{friend.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Deleted from Subscription')
        self.assertFalse(friend in self.user.get_requests())

    def test_requests_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        friend = User.objects.create_user(username='test_friend', password='testpassword')
        self.user.f_requests.add(friend)
        response = client.get('/api/requests/')
        self.assertEqual(response.data, [UserModelSerializer(friend).data])

    def test_followers_list(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        follower = User.objects.create_user(username='test_follower', password='testpassword')
        follower.f_requests.add(self.user.id)
        response = client.get('/api/followers/')
        self.assertEqual(response.data, [UserModelSerializer(follower).data])
