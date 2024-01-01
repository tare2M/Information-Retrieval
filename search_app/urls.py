from django.urls import path

from .views import search_results,home
urlpatterns = [
    path('', home, name='home'),
    path('search_results/', search_results, name='search_results'),
    # other URL patterns...
]
