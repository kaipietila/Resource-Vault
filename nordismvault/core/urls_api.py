from django.urls import path
from core.api.add_resource import ResourceApi
from core.api.contributor import ContributorApi

urlpatterns = [
    path('resource',
          ResourceApi.as_view(),
          name='resource_api'),
    path('contributor',
          ContributorApi.as_view(),
          name='contributor_api'),
]
