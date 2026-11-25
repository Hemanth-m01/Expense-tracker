from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ExpenseViewSet, SummaryView

router = SimpleRouter()
router.register('expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('summary/', SummaryView.as_view(), name='summary'),
    *router.urls,
]