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
    position = position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.user_link.name

    class Meta:
        ordering = ['position']
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

class Post(models.Model):
    title = models.CharField('Название', max_length = 50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField('Изображение', null=False, blank=False, upload_to="posts/")
    short_description = models.TextField('Краткое описание', null=True, blank=True)
    content = EditorJsJSONField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs = {'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class LinkPosts(models.Model):
    release_link = models.ForeignKey('Release', on_delete=models.CASCADE)
    post_link = models.OneToOneField(Post, on_delete=models.CASCADE, verbose_name='Пост')
    position = models.PositiveIntegerField(default=0, blank=False, null=False )

    def __str__(self):
        return self.post_link.title

    class Meta:
        ordering = ['position']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class Release(models.Model):

    visibility_choice = [
        (1, 'Видим'),
        (0, 'Скрыт')
    ]

    number = models.IntegerField('Номер выпуска', default=0)
    title = models.CharField('Название выпуска', max_length=50)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField('Описание выпуска')

    visibility = models.IntegerField("Видимость", choices=visibility_choice, default=False)

    bg_left_color = ColorField("Задний фон (Начало)",
    default='#ffc70080', format="hexa")
    bg_right_color = ColorField("Задний фон (Конец)",
    default='#ff7a0080', format="hexa")

    title_left_color = ColorField("Цвет заголовка (Начало)",
    default='#ff4d4d', format="hexa")
    title_right_color = ColorField("Цвет заголовка (Конец)",
    default='#ff7a0080', format="hexa")

    editor = models.ForeignKey(User,
        verbose_name='Главный редактор',
        on_delete=models.PROTECT,
        related_name='editor',
    )
    editor_words = models.TextField('Слова редактора')
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

        class PaginationButon:
            
            def __init__(self, post):
                self.slug = post.slug
                self.position = post.position
                self.disabled = post.disabled
                self.url = post.get_absolute_url()

        button_list = []
        slug_list = []
        posts_by_slug = {}
        now_ind = 0
        posts_links = LinkPosts.objects.filter(release_link=self).order_by('position')

        for post_l in posts_links:
            post = post_l.post_link
            post.position = post_l.position

            if slug == post.slug:
                post.disabled = False
            else:
                post.disabled = True

            posts_by_slug[post.slug] = PaginationButon(post)
            slug_list.append(post.slug)
        
        now_ind = slug_list.index(slug)
        if now_ind == 0:
            for i in range(now_ind, now_ind + 3):
                button_list.append(posts_by_slug[slug_list[i]])

        elif now_ind == 6:
            for i in range(now_ind - 2, now_ind + 1):
                button_list.append(posts_by_slug[slug_list[i]])
        
        else:
            for i in range(now_ind - 1, now_ind + 2):
                button_list.append(posts_by_slug[slug_list[i]])

        button_list.insert(0, posts_by_slug[slug_list[now_ind - 1]])
        
        if now_ind == len(slug_list)-1:
            button_list.insert(len(slug_list) + 1, posts_by_slug[slug_list[0]])
        else:
            button_list.insert(len(slug_list) + 1, posts_by_slug[slug_list[now_ind + 1]])
        
        return button_list

    class Meta:
        ordering = ['position']
        verbose_name = 'Выпуск'
        verbose_name_plural = 'Выпуски'
