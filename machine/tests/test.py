import os

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

THISDIR = os.path.dirname( __file__ )


class TestFileUpload(APITestCase):
    def setUp(self) -> None:
        # REST Client
        self.client = APIClient()

        # User for test
        self.user = User.objects.create_user( username='test_bot', password='12345' )
        self.client.force_login( self.user )
        # is_logined = self.client.login( username='test_bot', password='12345' )
        # self.assertTrue( is_logined )

        # Auth
        # token = Token.objects.get( user__username='lauren' )
        # self.client.credentials( HTTP_AUTHORIZATION='Token ' + token.key )

        # Force auth
        # self.user = user = User.objects.get(username='test_bot')
        # self.client.force_authenticate( user=self.user )


    def test_1_file_is_accepted(self):
        self.client.force_authenticate(self.user)

        file_url = os.path.join( THISDIR, "test-2.xls" )

        with open(file_url, 'rb') as f:
            response = self.client.post( '/api/machine/', {
                'name': "Test 1",
                'desc': "Desc 1",
                'input_file': f
            }, format="multipart" )

        self.assertEqual( status.HTTP_201_CREATED, response.status_code )

