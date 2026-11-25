from django.contrib import admin
from django.urls import include, path

from expenses.views import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
    path('api/', include('expenses.urls')),
]