import pytest
from rest_framework.test import APIClient

from expenses.models import Expense

pytestmark = pytest.mark.django_db

LIST_URL = '/api/expenses/'
SUMMARY_URL = '/api/summary/'


@pytest.fixture
def client():
    return APIClient()


def make_expense(title='Coffee', amount='3.50', category='food'):
    return Expense.objects.create(title=title, amount=amount, category=category)


def test_create_expense(client):
    response = client.post(LIST_URL, {'title': 'Lunch', 'amount': '12.50', 'category': 'Food'}, format='json')

    assert response.status_code == 201
    assert response.data['category'] == 'food'
    assert Expense.objects.count() == 1


@pytest.mark.parametrize('amount', ['0', '0.00', '-5'])
def test_create_rejects_non_positive_amount(client, amount):
    response = client.post(LIST_URL, {'title': 'Bad', 'amount': amount}, format='json')

    assert response.status_code == 400
    assert 'amount' in response.data
    assert Expense.objects.count() == 0


def test_list_returns_newest_first(client):
    make_expense(title='first')
    make_expense(title='second')

    response = client.get(LIST_URL)

    assert [item['title'] for item in response.data['results']] == ['second', 'first']


def test_filter_by_category_is_case_insensitive(client):
    make_expense(title='Coffee', category='food')
    make_expense(title='Bus', category='transport')

    response = client.get(LIST_URL, {'category': 'FOOD'})

    assert [item['title'] for item in response.data['results']] == ['Coffee']


def test_summary_totals_per_category(client):
    make_expense(title='Coffee', amount='3.50', category='food')
    make_expense(title='Lunch', amount='12.50', category='food')
    make_expense(title='Bus', amount='2.25', category='transport')

    response = client.get(SUMMARY_URL)

    assert response.data['total'] == '18.25'
    assert response.data['categories'] == [
        {'category': 'food', 'total': '16.00', 'count': 2},
        {'category': 'transport', 'total': '2.25', 'count': 1},
    ]