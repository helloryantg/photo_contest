from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('accounts/<int:id>/', views.my_account, name='my_account'),
    path('contests/<int:contest_id>/', views.photos_page, name='photos_page'),
    path('contests/create/', views.ContestCreate.as_view(), name='contests_create'),
    path('contests/<int:pk>/update/', views.ContestUpdate.as_view(), name='contests_update'),
    path('contests/<int:pk>/delete/', views.ContestDelete.as_view(), name='contests_delete'),
    path('posts/<int:contest_id>/create/', views.PostCreate.as_view(), name='posts_create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
    path('posts/<int:post_id>', views.posts_detail, name='posts_detail'),
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/update/', views.CommentUpdate.as_view(), name='comments_update'),
    path('comments/<int:pk>/delete/', views.CommentDelete.as_view(), name='comments_delete'),
]