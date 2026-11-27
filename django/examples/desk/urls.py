from django.urls import path
from . import views
app_name='desk'
urlpatterns=[path('',views.TaskList.as_view(),name='list'),path('new/',views.TaskCreate.as_view(),name='create'),
    path('tags/',views.TagList.as_view(),name='tags'),path('tags/<int:pk>/edit/',views.TagUpdate.as_view(),name='tag-update'),
    path('tags/<int:pk>/delete/',views.TagDelete.as_view(),name='tag-delete'),
    path('export/',views.ExportView.as_view(),name='export'),path('<int:pk>/',views.TaskDetail.as_view(),name='detail'),
    path('<int:pk>/edit/',views.TaskUpdate.as_view(),name='update'),path('<int:pk>/delete/',views.TaskDelete.as_view(),name='delete'),
    path('<int:pk>/complete/',views.complete,name='complete'),path('<int:pk>/upload/',views.upload,name='upload'),
    path('attachments/<int:pk>/',views.download,name='download')]
