from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsJSONField


class User(models.Model):
    name = models.CharField('Имя', max_length=50)
    image = models.ImageField('Изображение', upload_to="users/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class LinkUsers(models.Model):
    release_link = models.ForeignKey('Release', on_delete=models.CASCADE)
    user_link = models.ForeignKey(User, verbose_name='Участник', on_delete=models.CASCADE)
    role = models.CharField('Роль', max_length=30, null=True, blank=True)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.user_link.name

    class Meta:
        ordering = ['position']
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Post(models.Model):
    visibility_choice = [
        (1, 'Пост виден'),
        (0, 'Пост скрыт')
    ]

    title = models.CharField('Название', max_length=50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField('Изображение', null=True, blank=True, upload_to="posts/")
    short_description = models.TextField('Краткое описание', blank=True)
    content = EditorJsJSONField(default = dict, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class LinkPosts(models.Model):
    release_link = models.ForeignKey('Release', on_delete=models.CASCADE)
    post_link = models.OneToOneField(Post, on_delete=models.CASCADE, verbose_name='Пост')
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.post_link.title

    class Meta:
        ordering = ['-position']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PaginationButton:

    def __init__(self, post):
        self.title = post.title
        self.url = post.get_absolute_url()


class Release(models.Model):
    visibility_choice = [
        (1, 'Релиз видим'),
        (0, 'Релиз скрыт')
    ]

    number = models.IntegerField('Номер выпуска', default=1, null=True, blank=True, unique=True)
    title = models.CharField('Название выпуска', max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField('Описание выпуска', blank=True)

    visibility = models.IntegerField("Видимость", choices=visibility_choice, default=False)

    bg_left_color = ColorField("Задний фон (Начало)",
                               default='#ffc70080', format="hexa", null=True, blank=True)
    bg_right_color = ColorField("Задний фон (Конец)",
                                default='#ff7a0080', format="hexa", null=True, blank=True)

    title_left_color = ColorField("Цвет заголовка (Начало)",
                                  default='#ff4d4d', format="hexa", null=True, blank=True)
    title_right_color = ColorField("Цвет заголовка (Конец)",
                                   default='#ff7a0080', format="hexa", null=True, blank=True)

    editor = models.ForeignKey(User,
                               verbose_name='Главный редактор',
                               on_delete=models.PROTECT,
                               related_name='editor', 
                               null=True, blank=True
                               )
    editor_words = models.TextField('Слова редактора', blank=True)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('release', kwargs={'slug': self.slug})

    def get_release_members(self):
        members = LinkUsers.objects.filter(release_link=self).order_by('position')
        return members

    def get_release_posts(self):
        posts = []
        posts_links = LinkPosts.objects.filter(release_link=self).order_by('position')

        for post in posts_links:
            posts.append(post.post_link)

        return posts

    def get_pagination(self, slug):

        button_list = []
        slug_list = []
        posts_by_slug = {}
        posts_links = LinkPosts.objects.filter(release_link=self).order_by('position')

        for post_l in posts_links:
            post = post_l.post_link

            posts_by_slug[post.slug] = PaginationButton(post)
            slug_list.append(post.slug)
        
        now_ind = slug_list.index(slug)

        if len(slug_list) != 0:
            previous_post = posts_by_slug[slug_list[now_ind - 1]]
            button_list.append(previous_post)

        if len(slug_list) != now_ind + 1:
            subsequent_post = posts_by_slug[slug_list[now_ind + 1]]
        else:
            subsequent_post = posts_by_slug[slug_list[0]]
        
        button_list.append(subsequent_post)
        return button_list

    class Meta:
        ordering = ['-position']
        verbose_name = 'Выпуск'
        verbose_name_plural = 'Выпуски'
