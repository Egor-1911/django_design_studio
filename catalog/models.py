from django.db import models
from django.conf import settings

class DesignCategory(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория заявки'
        ordering = ['name']

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    ROOM_CHOICES = [
        ('living', 'Гостиная'),
        ('kitchen', 'Кухня'),
        ('bedroom', 'Спальня'),
        ('bathroom', 'Ванная'),
        ('office', 'Офис'),
        ('commercial', 'Коммерческое помещение'),
        ('other', 'Другое'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
    ]

    name = models.CharField('Имя', max_length=100, blank=True)
    room_type = models.CharField('Тип помещения', max_length=20, choices=ROOM_CHOICES)
    description = models.TextField('Описание задачи', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField( 'Фото помещения или план', upload_to='request_images/', blank=True, null=True)
    category = models.ForeignKey(DesignCategory, on_delete=models.CASCADE, null=True, verbose_name='Категория заявки')
    design_image = models.ImageField('Изображение дизайна', upload_to='design_results/', blank=True, null=True)
    admin_comment = models.TextField('Комментарий администратора', blank=True)

    def __str__(self):
        return "Заявка {self.name} — {self.get_room_type_display()}"


