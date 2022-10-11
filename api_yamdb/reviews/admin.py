from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title


class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)


class AdminGenre(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)


class AdminGenreInline(admin.TabularInline):
    model = GenreTitle


class AdminTitle(admin.ModelAdmin):
    fields = ('name', 'category', 'year',)
    readonly_fields = ('year',)
    inlines = (AdminGenreInline,)
    list_display = ('name', 'year', 'category', 'get_genres')
    search_fields = ('name', 'year', 'category__name', 'genre__name')
    list_filter = ('category', 'genre',)

    def get_genres(self, obj):
        return [genre.genre_id for genre in obj.genres.all()]
    get_genres.short_description = 'Жанр'


admin.site.register(Category, AdminCategory)
admin.site.register(Genre, AdminGenre)
admin.site.register(Title, AdminTitle)