from django.urls import path
from article.views import show_articles, create_article, json_all_article, json_id_article, delete_article,edit_article
app_name = 'article'

urlpatterns = [
    path("",show_articles,name="show_articles"),
    path("create/",create_article, name="create_article"),
    path("json-all/",json_all_article, name="json_all_article"),
    path("json-id/<uuid:id>",json_id_article, name="json_id_article"),
    path("delete/<uuid:id>",delete_article, name="delete_article"),
    path("edit/<uuid:id>",edit_article, name="edit_article"),
]