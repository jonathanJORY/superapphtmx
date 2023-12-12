from django.urls import path
from firsttuto import views
from django.contrib.auth.views import LogoutView

urlpatterns =[
    path('index/',views.IndexView.as_view(),name='index'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('tasks/',views.TaskList.as_view(),name='task-list'),
]

htmx_views = [
    path('check_username/',views.check_username,name='check_username'),
    path('add-task/',views.add_task,name='add-task'),
    path('delete-task/<int:pk>',views.delete_task,name='delete-task'),
    path('search-task/',views.search_task,name='search-task'),
    path('clear/',views.clear,name='clear'),
    path('sort/',views.sort,name='sort'),

]

urlpatterns += htmx_views