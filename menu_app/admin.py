from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    """Вспомогательный класс, для встаивания одной модели в другую"""

    model = MenuItem
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Админ-класс для модели Меню"""

    list_display = ("name",)
    inlines = [
        MenuItemInline,
    ]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Админ-класс для модели Пункта меню"""

    list_display = ("title", "menu", "parent", "url", "named_url")
    list_filter = ("menu",)
