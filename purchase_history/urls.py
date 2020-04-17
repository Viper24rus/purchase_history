from django.urls import path, include

urlpatterns = [
    path('', include('top_customers.urls')),
]
