from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.list, name="list"),
    path('create/', views.create, name="create"),
    path('<int:post_id>/', views.read, name="read"),
    path('<int:post_id>/update', views.update, name="update"),
    path('<int:post_id>/delete', views.delete, name="delete"),
    path('<int:post_id>/like', views.like, name="like"), # url엔 post_id만 넘겨주고, user관한 정보는 view에서 처리
    path('<int:post_id>/comment/create/', views.create_comment, name="comment"),
]