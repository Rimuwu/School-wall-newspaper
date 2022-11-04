from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsJSONField

class User(models.Model):
    name = models.CharField('Имя', max_length = 50)
    image = models.ImageField('Изображение', upload_to="users/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

class LinkUsers(models.Model):
    release_link = models.ForeignKey('Release', on_delete = models.CASCADE)

    user_link = models.ForeignKey(User, verbose_name = 'Участник', on_delete = models.CASCADE)
    role = models.CharField('Роль', max_length = 30, null = True, blank = True)

    position = position = models.PositiveIntegerField(default = 0 ,blank = False, null = False )

    def __str__(self):
        return self.user_link.name

    class Meta:
        ordering = ['position']
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

class Post(models.Model):
    title = models.CharField('Название', max_length = 50)
    image = models.ImageField('Изображение', null = False, blank = False, upload_to="posts/")
    short_description = models.TextField('Краткое описание', null = True, blank = True)
    content = EditorJsJSONField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs = {'post_id': self.pk} )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class LinkPosts(models.Model):
    release_link = models.ForeignKey('Release', on_delete = models.CASCADE)
    post_link = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = 'Пост')
    position = position = models.PositiveIntegerField(default = 0 ,blank = False, null = False )

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

    number = models.IntegerField('Номер выпуска', default = 0)
    title = models.CharField('Название выпуска', max_length = 50)
    description = models.TextField('Описание выпуска')

    visibility = models.IntegerField("Видимость", choices = visibility_choice, default = False)

    bg_left_color = ColorField("Задний фон (Начало)",
    default = '#ffc70080', format = "hexa")
    bg_right_color = ColorField("Задний фон (Конец)",
    default = '#ff7a0080', format = "hexa")

    title_left_color = ColorField("Цвет заголовка (Начало)",
    default = '#ff4d4d', format = "hexa")
    title_right_color = ColorField("Цвет заголовка (Конец)",
    default = '#ff7a0080', format = "hexa")

    editor = models.ForeignKey(User,
        verbose_name = 'Главный редактор',
        on_delete = models.PROTECT,
        related_name = 'editor',
    )
    editor_words = models.TextField('Слова редактора')
    position = models.PositiveIntegerField( default = 0, blank = False, null = False)

    def __str__(self):

        if self.position == 1:
            posit = 'Главный'
        else:
            posit = self.position

        return f'({posit}) {self.title}'

    def get_absolute_url(self):
        return reverse('release', kwargs = {'release_id': self.pk} )

    class Meta:
        ordering = ['position']
        verbose_name = 'Выпуск'
        verbose_name_plural = 'Выпуски'
