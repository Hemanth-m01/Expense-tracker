from django.shortcuts import render
from rest_framework import viewsets

from .models import Expense
from .serializers import ExpenseSerializer

from decimal import Decimal

from django.db import connection
from django.db.models import Count, Sum
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

TWO_PLACES = Decimal('0.01')


class SummaryView(APIView):
    def get(self, request):
        rows = (
            Expense.objects.values('category')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('category')
        )
        categories = [
            {
                'category': row['category'],
                'total': str(row['total'].quantize(TWO_PLACES)),
                'count': row['count'],
            }
            for row in rows
        ]
        overall = sum((row['total'] for row in rows), Decimal('0'))
        return Response(
            {
                'total': str(overall.quantize(TWO_PLACES)),
                'count': sum(row['count'] for row in rows),
                'categories': categories,
            }
        )


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:
        return JsonResponse({'status': 'unavailable'}, status=503)
    return JsonResponse({'status': 'ok'})

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        queryset = Expense.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category.strip().lower())
        return queryset