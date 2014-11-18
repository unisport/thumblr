from django.contrib import admin
from django.utils.safestring import mark_safe
from thumblr.dto import ImageUrlSpec
from thumblr.models import Image, ImageFile, ImageSize
from thumblr.services.image_file_service import get_image_file_url


class ImageAdmin(admin.ModelAdmin):
    list_filter = ('site', 'content_type',)


class ImageFileAdmin(admin.ModelAdmin):
    readonly_fields = ('image_hash', 'image_hash_in_storage', 'cdn_url', 's3_url')
    list_filter = ('size',)

    def cdn_url(self, obj):
        return mark_safe(
            u"<a href='{url}'>{url}</a>".format(
                url=get_image_file_url(obj, ImageUrlSpec.CDN_URL)
            )
        )

    def s3_url(self, obj):
        return mark_safe(
            u"<a href='{url}'>{url}</a>".format(
                url=get_image_file_url(obj, ImageUrlSpec.S3_URL)
            )
        )


class ImageSizeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(ImageSize, ImageSizeAdmin)

