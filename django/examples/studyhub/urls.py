from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include,path
from rest_framework.routers import DefaultRouter
from desk import views
from desk.api import TaskViewSet
router=DefaultRouter();router.register('tasks',TaskViewSet,basename='api-task')
urlpatterns=[path('',views.TaskList.as_view(),name='home'),path('health/',views.health,name='health'),
    path('async-health/',views.async_health,name='async-health'),path('tasks/',include('desk.urls')),
    path('accounts/signup/',views.SignupView.as_view(),name='signup'),
    path('accounts/login/',auth_views.LoginView.as_view(),name='login'),
    path('accounts/logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('accounts/',include('django.contrib.auth.urls')),path('admin/',admin.site.urls),path('api/v1/',include(router.urls))]
