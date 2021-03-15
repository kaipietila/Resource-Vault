from django.urls import path

from core.views.home import home
from core.views.resource import add_resource_view
from core.views.user_management import login_view, logout_view, signup_view


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
]
