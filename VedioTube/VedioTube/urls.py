"""VedioTube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name = "index"),
    path('watch/<str:vid>/',views.watch,name="watch"),
    path("about/",views.about,name="About"),
    # path("uploadfile/",views.uploadfile,name="uploadfile"),
    path("upload/",views.upload,name="upload"),
    # path("loginfile/",views.loginfile,name="loginfile"),
    path("login/",views.login,name="login"),
    # path("registerpage/",views.registerpage,name="registerpage"),
    path("register/",views.register,name="register"),
    path("cpasswordpage/",views.cpasswordpage,name="cpasswordpage"),
    path("cpasswordsave/",views.cpasswordsave,name="cpasswordsave"),
    path("search/",views.search,name="search"),
    path("logout/",views.logout,name="logout"),
    path('post_likes/<str:vid>',views.post_likes,name="post_likes"),
    path('post_dislikes/<str:vid>',views.post_dislikes,name="post_dislikes"),
    path('post_comments/<str:vid>',views.post_comments,name="post_comments"),
    # path("csv_file/",views.csv_file,name="csv_file"),
    path("subscribe/",views.subscribe,name="subscribe"),
    path("romance/",views.romance,name="romance"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)