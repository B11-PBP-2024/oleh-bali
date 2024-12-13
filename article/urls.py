from django.urls import path
from article.views import delete_mobile, edit_article_mobile, show_articles, create_article, json_all_article, json_id_article, delete_article,edit_article,json_user_article, create_article_flutter
app_name = 'article'

urlpatterns = [
    path("",show_articles,name="show_articles"),
    path("create/",create_article, name="create_article"),
    path("json-all/",json_all_article, name="json_all_article"),
    path("json-user/",json_user_article, name="json_user_article"),
    path("json-id/<uuid:id>",json_id_article, name="json_id_article"),
    path("delete/<uuid:id>",delete_article, name="delete_article"),
    path("delete/mobile/<uuid:id>/",delete_mobile, name="delete_mobile"),
    path("edit/<uuid:id>",edit_article, name="edit_article"),
    path("edit/mobile/<uuid:id>/",edit_article_mobile, name="edit_article_mobile"),
    path("create/mobile",create_article_flutter, name="create_article_flutter"),
]