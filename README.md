#Thumblr [![Build Status](https://magnum.travis-ci.com/unisport/thumblr.svg?token=qsbi8v1ehwb8Bju5YWQ6&branch=master)](https://magnum.travis-ci.com/unisport/thumblr)

Thumblr is an app that provides an abstraction to deal with images throughout the storefront project. The image below illustates the components involved.  

![](http://s3.amazonaws.com/storefront-dump/upload.png)


The upload interface is accepts files as an input.  
It takes care of the following steps:

* The original file gets uploaded to S3
* A renamed hash is generated based on the contents of the file
* Relevant information about the file is saved to the database
* The file is served via cloudfront with a far future expire

The table in which such data is saved have the following main attributes:

    class Image(models.Model):
        content_object = model.GenericForeignKey()
        
        image_hash = model.CharField()
        
        hashed_image_in_storage = model.ImageField(storage=s3)
        image_in_storage = model.ImageField(storage=s3)        

        is_main = model.BooleanField()
        order_number = model.PositiveInteger()
        

The images could then be retrieved using a simple query like:

        Images.objects.filter(content_type='articles', object_id=article_id, site_id=site_id) 

Such a system allow us to save any type of file. 

####Usage

###Template tags
    {% load thumblr_tags %}
    
    <img src='{% thumblr 'boots.jpg' size='original' content_type_name='image' %}' />

    {% load thumblr_tags %}
    {% thumblr_imgs size='original' as imgs %}
    {% for img_url in imgs %}
        <img src='{{ img_url }}' />
    {% endfor %}
    
###API

Main purposes are covered with use cases, data should be provided with dto's 
`ImageMetadata`, `ImageUrlSpec`. All this available from root package `thumblr`:

    import thumblr
    
    thumblr.add_image(
        uploaded_file, 
        thumblr.ImageMetadata(file_name='photo.jpg', ...)
    )
    images_dtos = thumblr.get_all_images(
        thumblr.ImageMetadata(object_id=1, content_type_id=1)
    )
    thumblr.get_image_url(
        thumblr.ImageMetadata(object_id=1, content_type_id=1, size_slug='original'), 
        thumblr.ImageUrlSpec.S3
    )
    
Uploaded file by itself should be provided as *django* *File*. 
*ImageMetadata* - is a silver bullet of thumblr app. It represents file data (returned by *add_image*, *get_all_images*, etc.), 
with it you could specify a *filter* from *get_all_images*.

### Image processing
There also couple of utils for image processing: 
 * Cropping, thumbnailing, watermarking, bubbles, ...

All this is placed in `thumblr.image_processing`. To prepare image for processing you may need functionality to convert
ImageMetadata to Pillow Image and vice versa to work further. This functions are available in `thumblr.image_processing.context_mapping` 


####Installation
First ensure that you have a valid ssh keys. Than install the application with:

        pip install git+ssh://git@github.com/unisport/thumblr.git

####Setup
1. Add thumblr to installed apps:

        INSTALLED_APPS = (
          ...
          'thumblr',
        )
        
2. Add to settings 
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
        AWS_THUMBLR_BUCKET = os.environ.get('AWS_THUMBLR_BUCKET', 'thumblr-testing')        

3. Add admin to urls. In this case you will be able to add image sizes
        url(r'^admin/', include(admin.site.urls)),
        
