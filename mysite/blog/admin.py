from django.contrib import admin
from .models import Article, ArticleComment


class CommentInline(admin.TabularInline):
    model = ArticleComment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'content')
    list_editable = ('user',)
    inlines = [CommentInline]


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'created', 'comment')
    list_editable = ('reviewer', 'comment')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
