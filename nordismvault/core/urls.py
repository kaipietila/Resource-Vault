from django.urls import path

from core.views.home import home
from core.views.user_management import login_view
from core.views.user_management import logout_view
from core.api.resource import ResourceApi
from core.api.contributor import ContributorApi
from core.api.resource import UploadResource
from core.api.invitation import InvitationRequestApi


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
     path('api/resource/',
          ResourceApi.as_view(),
          name='resource_api'),
     path('api/resource/upload/',
          UploadResource.as_view(),
          name='upload_resource_api'),
     path('contributor',
          ContributorApi.as_view(),
          name='contributor_api'), 
     path('login/api/invitation/',
          InvitationRequestApi.as_view(),
          name='invitation_api'),           
]
