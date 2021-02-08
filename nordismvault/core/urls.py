from django.urls import path

from core.views import add_resource_view, success_view

urlpatterns = [
    path('add-resource/',
         add_resource_view,
         name='core-add-resource'),
    path('success/',
         success_view,
         name='core-success'),
    path('error/',
         success_view,
         name='core-error'),
]
