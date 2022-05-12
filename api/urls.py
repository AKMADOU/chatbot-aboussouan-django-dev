from rest_framework import routers
#from quartier.views import QuartierViewSet,VideosViewSet
from django.conf.urls import url, include
from . import views


from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token, verify_jwt_token
#voir signets
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView,
)
from rest_framework.authtoken import views as vw
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token, verify_jwt_token
from django.conf.urls.static import static


urlpatterns = [ 
    url(r'^auth/login/$', obtain_jwt_token),
    url(r'^auth/register/$', views.UserRegisterView.as_view()),

    url(r'^url/(?P<id>[0-9]+)/$', views.UrlAPIView.as_view()),
    url(r'^url/$', views.UrlAPIListView.as_view()),
    
    
    url(r'^user/(?P<id>[0-9]+)/$', views.UserAPIView.as_view()),
    url(r'^user/$', views.UserAPIListView.as_view()),


    
    url(r'^urlbyword/$', views.UrlByWordAPIView.as_view()),
    
    url(r'^audiobyword/$', views.AudioByWordAPIView.as_view()),
   

    
   # url(r'^videosbymotcle/(?P<mot_cle>[-a-zA-Z0-9.`?{}]+)/$', views.VideoByMotCleAPIView.as_view()),
    
    #url(r'^videobyquartier/(?P<id>[0-9]+)/$', views.VideosByQuartierAPIView.as_view()),
    #url(r'^audiobyquartier/$', views.AudioByQuartierAPIView.as_view()),
   

]





