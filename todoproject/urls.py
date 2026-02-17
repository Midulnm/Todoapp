from django.contrib import admin
from django.urls import path
from todoapp.views import home   # import directly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),   # directly connect view
]
