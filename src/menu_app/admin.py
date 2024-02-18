from django.contrib import admin

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    list_filter = ['parent']
    search_fields = ('title', 'parent__title')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                kwargs["queryset"] = self.model.objects.exclude(id=obj_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
