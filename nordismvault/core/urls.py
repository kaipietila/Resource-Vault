from django.urls import path

from core.views.home import home
from core.views.resource import add_resource_view
from core.views.user_management import login_view, logout_view, signup_view
from core.api.resource import ResourceApi
from core.api.contributor import ContributorApi
from core.api.resource import UploadResource


urlpatterns = [
    path('add-resource/',
         add_resource_view,
         name='core-add-resource'),
    path('',
         home,
         name='home'),
    path('login/',
        login_view,
         name='login_user'),
    path('logout/',
        logout_view,
         name='logout_user'),
    path('signup/',
         signup_view,
         name='signup_user'),
     path('api/resource/',
          ResourceApi.as_view(),
          name='resource_api'),
    path('api/resource/upload/',
          UploadResource.as_view(),
          name='upload_resource_api'),
    path('login/api/contributor/',
          ContributorApi.as_view(),
          name='contributor_api'),         
]
