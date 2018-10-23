"""hasker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from user.views import SignupView, SignupDoneView, UserSettingsView
from question.models import Trend
from question.views import IndexView, AskView, QuestionView, QuestionListView, VoteView, BestAnswerView, SearchView, TagView
from api.views import IndexViewSet, TrendingViewSet, SearchViewSet, QuestionViewSet

router = routers.DefaultRouter()
router.register(r'(?P<version>(v1|v2))/index', IndexViewSet)
router.register(r'(?P<version>(v1|v2))/trending', TrendingViewSet)
router.register(r'(?P<version>(v1|v2))/search', SearchViewSet, basename='search-list')
router.register(r'(?P<version>(v1|v2))/questions', QuestionViewSet, basename='question-detail')

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        extra_context={"trends": Trend.get_trends()}
    )),
    path('logout/', auth_views.LogoutView.as_view()),
    path('signup/', SignupView.as_view()),
    path('signup/done/', SignupDoneView.as_view()),
    path('settings/', UserSettingsView.as_view()),
    path('ask/', AskView.as_view()),
    path('question/<int:id>/', QuestionView.as_view(), name="question"),
    path('question/vote/', VoteView.as_view(), name="question_vote"),
    path('question/best/', BestAnswerView.as_view(), name="question_best"),
    path('question/list/', QuestionListView.as_view(), name="question_vote"),
    path('search/', SearchView.as_view(), name="question_search"),
    path('tag/<str:tag>/', TagView.as_view(), name="question_tag"),
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
   #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', IndexView.as_view()),
]
