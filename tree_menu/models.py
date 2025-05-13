from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify


class MenuItem(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название пункта меню')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительский пункт'
    )
    url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='URL или named URL'
    )
    named_url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Named URL',
        help_text='Именованный URL из urls.py'
    )
    menu_name = models.CharField(
        max_length=50,
        verbose_name='Название меню',
        help_text='Название меню, к которому относится этот пункт'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.named_url
        return self.url or '#'

    def save(self, *args, **kwargs):
        if not self.url and not self.named_url:
            self.url = f'/{slugify(self.name)}/'
        super().save(*args, **kwargs)