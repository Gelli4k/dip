import pytest
from rest_framework.test import APIClient


@pytest_fixture
def auth_client():
    client = APIClient()
    client.login(username='john', password='test123')
