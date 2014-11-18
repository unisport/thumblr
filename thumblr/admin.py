from django.contrib import admin
from thumblr.models import Image, ImageFile, ImageSize


class ImageAdmin(admin.ModelAdmin):
    pass


class ImageFileAdmin(admin.ModelAdmin):
    readonly_fields = ('image_hash', 'image_hash_in_storage')


class ImageSizeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(ImageSize, ImageSizeAdmin)

