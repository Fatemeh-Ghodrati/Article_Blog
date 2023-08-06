from django.contrib import admin
from .models import Article, Category

# Register your models here.
def make_published(modelAdmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modelAdmin.message_user(request, "{}  مقاله {}".format(rows_updated, message_bit))
make_published.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modelAdmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = "پیش نویس شد."
    else:
        message_bit = "پیش نویس شدند."
    modelAdmin.message_user(request, "{}  مقاله {}".format(rows_updated, message_bit))
make_draft.short_description = "پیش نویس شدن مقالات انتخاب شده"

def make_active(modelAdmin, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message_bit = "فعال شد"
    else:
        message_bit = "فعال شدند."
    modelAdmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))
make_active.short_description = "فعال شدن دسته بندی های انتخاب شده"

def make_inactive(modelAdmin, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        message_bit = "غیر فعال شد."
    else:
        message_bit = "غیر فعال شدند."
    modelAdmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))
make_inactive.short_description = "غیر فعال شدن دسته بندی های انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position','title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_active, make_inactive]

admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag','author', 'slug', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_published, make_draft]

    def category_to_str(self, obj):
        return "، ".join([category.title for category in obj.category.active()])
    category_to_str.short_description = "عنوان دسته بندی"

admin.site.register(Article, ArticleAdmin)