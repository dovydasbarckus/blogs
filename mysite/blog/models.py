from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db import models


class Article(models.Model):
    title = models.CharField("Title", max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    content = HTMLField('Content', null=True, blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    @property
    def total_sum(self):
        comments = ArticleComment.objects.filter(article_id=self.id)
        return len(comments)

    @property
    def sentence(self):
        words = self.content[:120]
        words += "..."
        return words


class ArticleComment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='comments')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField('Comment', max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f'{self.reviewer} {self.comment}'


