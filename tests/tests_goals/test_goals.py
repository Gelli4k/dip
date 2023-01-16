from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_goal(auth_client, category):
    url = reverse('goal_create')
    test_date = str(datetime.now().date())
    payload = {
            'title': 'New goal',
            'category': category.pk,
            'description': 'This is a nice goal to have',
            'due_date': test_date,

        }

    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']

def test_add():
    assert 1 == 1
