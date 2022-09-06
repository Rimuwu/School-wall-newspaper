from django.db import models
from django.utils import timezone
from django.urls import reverse

class Note( models.Model ):
    note_type = [
        ('note', 'Просто запись'),
        ('anime', 'Мнение о аниме'),
        ('manga', 'Мнение о манге'),
        ('film', 'Мнение о фильме'),
        ('book', 'Мнение о книге'),
        ('project', 'Проект'),
        ('info', 'Информация о себе'),
        ('other', 'Другое'),
    ]

    stars = [
        (10,'(10) Великолпепно'),
        (9, '(9) Восхитительно'),
        (8, '(8) Супер'),
        (7, '(7) Хорошо'),
        (6, '(6) Неплохо'),
        (5, '(5) Нормально'),
        (4, '(4) Боле менее'),
        (3, '(3) Плохо'),
        (2, '(2) Очень плохо'),
        (1, '(1) Ужасно'),
        (0, 'Без оценки'),
    ]

    title = models.CharField('Название', max_length = 50)
    text = models.TextField('Описание')
    image = models.ImageField('Изображение', null=True, blank=True, upload_to="notes_images/")
    num_stars = models.IntegerField('Оценка', choices = stars, default = 5)
    note_type = models.CharField('Тип записи', choices = note_type, default = 'other', max_length = 10)
    created_date = models.DateTimeField('Дата', default=timezone.now)

    def __str__(self):
        return f'{self.title} ({self.note_type})'

    def get_absolute_url(self):
        return reverse('post', kwargs = {'post_id': self.pk} )
        #pk - id из базы

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
