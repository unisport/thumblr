from django.contrib import admin
from django.utils.safestring import mark_safe
from thumblr.services.url import get_image_instance_url
from thumblr.dto import ImageUrlSpec
from thumblr.models import Image, ImageSize


class ImageAdmin(admin.ModelAdmin):
    list_filter = ('site', 'content_type', 'size')
    readonly_fields = ('image_hash', 'image_hash_in_storage', 'cdn_url', 's3_url')

    def cdn_url(self, obj):
        return mark_safe(
            u"<a target='_blank' href='{url}'>{url}</a>".format(
                url=get_image_instance_url(obj, ImageUrlSpec.CDN_URL)
            )
        )

    def s3_url(self, obj):
        return mark_safe(
            u"<a target='_blank' href='{url}'>{url}</a>".format(
                url=get_image_instance_url(obj, ImageUrlSpec.S3_URL)
            )
        )


class ImageSizeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageSize, ImageSizeAdmin)

