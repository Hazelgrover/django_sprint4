from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class BaseInfo(models.Model):
    name = models.CharField('
Название', max_length=256)
    slug = models.SlugField('
Слаг', unique=True)
    description = models.TextField('
Описание', blank=True)

    class Meta:
        abstract = True
        verbose_name = '
Базовая информация'
        verbose_name_plural = '
Базовая информация'

    def __str__(self):
        return self.name

class Location(BaseInfo):
    class Meta:
        verbose_name = '
Город'
        verbose_name_plural = '
Города'

class Category(BaseInfo):
    class Meta:
        verbose_name = '
Тип номера'
        verbose_name_plural = '
Типы номеров'

class Room(models.Model):
    title = models.CharField('
Название номера', max_length=255)
    description = models.TextField('
Описание')
    pub_date = models.DateTimeField('
Дата публикации', default=timezone.now)
    image = models.ImageField('
Фото номера', upload_to='rooms/', blank=True, null=True)
    author = models.ForeignKey(User, verbose_name='
Администратор', on_delete=models.CASCADE, related_name='rooms')
    category = models.ForeignKey(
        Category, verbose_name='
Тип номера',
        on_delete=models.SET_NULL, null=True, related_name='rooms'
    )
    location = models.ForeignKey(
        Location, verbose_name='
Город',
        on_delete=models.SET_NULL, null=True, related_name='rooms'
    )
    is_published = models.BooleanField('
Опубликован', default=True)
    created_at = models.DateTimeField('
Создано', auto_now_add=True)

    class Meta:
        verbose_name = '
Номер'
        verbose_name_plural = '
Номера'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

class Review(models.Model):
    room = models.ForeignKey(Room, verbose_name='
Номер', on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, verbose_name='
Гость', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('
Отзыв')
    created_at = models.DateTimeField('
Дата создания', auto_now_add=True)
    edited_at = models.DateTimeField('
Дата изменения', null=True, blank=True)

    class Meta:
        verbose_name = '
Отзыв'
        verbose_name_plural = '
Отзывы'
        ordering = ('created_at',)

    def __str__(self):
        return f'
Отзыв {self.author} о {self.room}'