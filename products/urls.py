from django.urls import path

from .views import ProductList


urlpatterns = [
    path('list/', ProductList.as_view()),
]