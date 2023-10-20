from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from apps.blog.models import Blog


def blog_list() -> QuerySet[Blog]:
    qs = Blog.objects.select_related('author').all()
    return qs