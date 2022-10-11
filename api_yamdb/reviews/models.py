from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Сами письмена отзыва'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
        help_text='день-месяц-год'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Автор отзыва',
        help_text='Привязка к автору отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Произведение',
        help_text='К какому произведению отзыв'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Сами письмена комента'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
        help_text='день-месяц-год'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Привязка к автору комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий к отзыву',
        help_text='К какому отзыву коммент'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]

class Point(models.Model):
    #Нужно продумать запрет на многоразовое добавление оценки
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='raiting_point',
        verbose_name='оценка произведения',
        help_text='выставленный поизведению балл'
    )

    weight = models.IntegerField(
        verbose_name='Оценка произведения',
        help_text='Число от 1 до 10 для оценивания'
    )

    #Продумываю запрет ставить повторную оценку произведению
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'weight'),
                name='unique point'),
            models.CheckConstraint(
                check=~models.Q(user=models.F('user')),
                name='do not repeatpoint'),
        ]