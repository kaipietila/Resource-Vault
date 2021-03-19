from django.urls import path

from core.views.home import home
from core.views.user_management import login_view, logout_view, signup_view
from core.api.resource import ResourceApi
from core.api.contributor import SignUpApi
from core.api.resource import UploadResource


urlpatterns = [
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
    path('login/api/signup/',
          SignUpApi.as_view(),
          name='signup_api'),         
]
