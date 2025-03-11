from django.urls import path
from .views import TaskListView, TaskCreateView, TaskCompleteView, TaskDeleteView, user_login, user_logout, register

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('add/', TaskCreateView.as_view(), name='add_task'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='complete_task'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
]