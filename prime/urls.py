from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

import profiles.views as pro_views

router = routers.DefaultRouter()
# router.register(r'add-client', sud_views.AddClient)

app_name = 'profiles'
urlpatterns = [
    # url(r'^', include(router.urls)),

    path('login/', pro_views.UserLogin.as_view()),
    path('logout/', pro_views.UserLogout.as_view()),
    path('create/', pro_views.CreateUser.as_view()),
    # path('client/create/<int:id>/', sud_views.ClientDetail.as_view()),

    # path('list-subjects/', sud_views.ListSubject.as_view()),
    # path('create-subjects/', sud_views.SubjectDetail.as_view()),
    # path('create-subjects/<int:id>/', sud_views.SubjectDetail.as_view()),

    # path('list-standards/', sud_views.ListStandard.as_view()),
    # path('create-standards/', sud_views.StandardDetail.as_view()),
    # path('create-standards/<int:id>/', sud_views.StandardDetail.as_view()),

    # path('list-substds/', sud_views.ListSubStd.as_view()),
    # path('create-substds/', sud_views.SubStdDetail.as_view()),
    # path('create-substds/<int:id>/', sud_views.SubStdDetail.as_view()),

    # path('list-chapters/', sud_views.ListChapter.as_view()),
    # path('create-chapters/', sud_views.ChapterDetail.as_view()),
    # path('create-chapters/<int:id>/', sud_views.ChapterDetail.as_view()),

    # path('list-topics/', sud_views.ListTopic.as_view()),
    # path('create-topics/', sud_views.TopicDetail.as_view()),
    # path('create-topics/<int:id>/', sud_views.TopicDetail.as_view()),

    # path('list-questions/', sud_views.ListQuestion.as_view()),
    # path('create-questions/', sud_views.QuestionDetail.as_view()),
    # path('create-questions/<int:id>/', sud_views.QuestionDetail.as_view()),
    # path('bulk-upload-questions/', sud_views.BulkUploadQuestion.as_view()),
    
]