from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Title cannot be blank.')
        return value

    def validate_category(self, value):
        return value.strip().lower() or 'other'