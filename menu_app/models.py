from django.db import models
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class Menu(models.Model):
    """Модель меню"""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель пункта меню"""

    title = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, related_name="items", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )

    # Сырой url
    url = models.CharField(max_length=200, null=True, blank=True)

    # Наименование url
    # При заполнении этого поля необходимо прописать наименования и в urls.py
    named_url = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return "#"
        return self.url or "#"

    def __str__(self):
        return self.title
