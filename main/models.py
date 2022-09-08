from django.db import models
from django.utils import timezone
from django.urls import reverse


class Note( models.Model ):
    note_type = [
        ('school_projects', 'Школьные проекты'),
        ('school_news', 'Школьные новости'),
        ('important', 'Разговор о важном'),
        ('journalism', 'Журналистика'),
        ('birthday', 'День рождения'),
        ('game', 'Игры'),
        ('other', 'Дургое')
    ]

    title = models.CharField('Название', max_length = 50)

    text = models.TextField('Краткое описание')
    image = models.ImageField('Изображение', null=True, blank=True, upload_to="notes_images/")
    note_type = models.CharField('Категория', choices = note_type, default = 'other', max_length = 15)
    content = models.TextField('Контент страницы')

    created_date = models.DateTimeField('Дата', default = timezone.now)

    def __str__(self):
        return f'{self.title} ({self.note_type})'

    def get_absolute_url(self):
        return reverse('post', kwargs = {'post_id': self.pk} )
        #pk - id из базы

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
