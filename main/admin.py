from adminsortable2.admin import SortableAdminMixin, SortableTabularInline
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Release, User, LinkPosts, LinkUsers

class PostInline(SortableTabularInline):
    model = LinkPosts

class UserInline(SortableTabularInline):
    model = LinkUsers

@admin.register(Release)
class PostAdmin(SortableAdminMixin, admin.ModelAdmin):
    
    list_display = ('title', 'editor', 'pk_show')
    list_per_page = 10
    inlines = [ PostInline, UserInline ]

    def pk_show(self, release):
        return mark_safe(f'<a href="{release.get_absolute_url()}">Выпуск {release.number}</a>')

    pk_show.short_description = 'Страница просмотра'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['get_image', 'title', 'pk_show']
    list_per_page = 7

    def pk_show(self, post):
         return mark_safe(f'<a href="{post.get_absolute_url()}">Пост {post.pk}</a>')

    pk_show.short_description = 'Страница просмотра'

    def get_image(self, post):
        return mark_safe('<image src="%s" width="100" />' % post.image.url)

    get_image.short_description = 'Изображение'

@admin.register(User)
class PostAdmin(admin.ModelAdmin):

    list_display = ['get_image', 'name']
    list_per_page = 10

    def get_image(self, user):
        return mark_safe('<image src="%s" width="100" />' % user.image.url)

    get_image.short_description = 'Изображение'