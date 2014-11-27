#Thumblr

Thumblr is an app that provides an abstraction to deal with images throughout the storefront project. The image below illustates the components involved.  

![](http://s3.amazonaws.com/storefront-dump/upload.png)


The upload interface is  accepts files as an input.  
It takes care of the following steps:

* The original file gets uploaded to S3
* A renamed hash is generated based on the contents of the file
* Relevant information about the file is saved to the database
* The file is served via cloudfront with a far future expire

The table in which such data is saved could have the following attributes.

![](http://s3.amazonaws.com/storefront-dump/model.png)
 

The images could then be retrieved using a simple query like:

        Images.objects.filter(content_type='articles', object_id=article_id, site_id=site_id) 

Such a system should allow us to save any type of file. 

####The proposition

There are many ways to go about solving such a problem. We do however have solutions within our toolbox to solve this particular issue. Eg. Django provides some abstractions. 

1. [The File class](https://docs.djangoproject.com/en/dev/ref/files/file/#django.core.files.File)
A wrapper around the file object, which can be used to manipulate something that is represented as a file.

2. [The Storage class](https://docs.djangoproject.com/en/dev/ref/files/storage/#the-storage-class)
This represents the location where the file needs to be stored. The default is of cause having it stored in the same machine as the code running it. This can however be easily extended.
Here is a library that does just that [django-storages](http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html)

3. [CachedStaticFilesStorage](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#django.contrib.staticfiles.storage.CachedStaticFilesStorage)
Is mechanism that calculates the hash and stores it in the caching system installed.
The post process technique used is interesting as one would not necessarily have the cached value at hand at all times, so by guessing the file key eg. {% static 'product_id.jpg' %} django will use that value to locate the file, re-calculate the hash value and save it to its cache.  All the subsequent requests will have the hashed file served. 

It seems as though the problem is solved. There is however challenges in wiring this all together and customising these components to work as described. 
I'm thinking it could be useful if we split responsibility into 2-3 subsystems.

![](http://s3.amazonaws.com/storefront-dump/H3r36G9.png)


#####Thumblr's Responsibility
* Manipulation (cropping, overlaying, resize, file-format conversion, feature-x)
* Far future expire URLs with domain-alternation (static-0,static-1,static-n...).unisport.dk

#####API's proveded Responsibility

 * image-api manipulation/fetching
 * image-api for cropping
 * image-api upload images




So in phase 1 we want an app that exposes the api described above, with which we can use to create phase 2. 

The most important aspect for us is that we have a standardized API that we can further extend when the need arises. 

####Installation
First ensure that you have a valid ssh keys. Than install the application with:

        pip install git+ssh://git@github.com/unisport/thumblr.git

####Setup
1. Add thumblr to installed apps:

        INSTALLED_APPS = (
          ...
          'django_tables2',
          'thumblr',
        )
        
2. Add to settings 

        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
        AWS_THUMBLR_BUCKET = os.environ.get('AWS_THUMBLR_BUCKET', 'thumblr-testing')        

3. Add to settings TEMPLATE_CONTEXT_PROCESSORS

        TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
        )
        
4. Add environment variables related to AWS and S3 bucket
        
        AWS_ACCESS_KEY_ID="..."
        AWS_SECRET_ACCESS_KEY="..."
        AWS_THUMBLR_BUCKET="..."
        
5. Add admin to urls. In this case you will be able to add image sizes
        
        url(r'^admin/', include(admin.site.urls)),
        
6. urlpatterns = patterns('image_tiles',
       url(r'^create/$', views.create_tile, {'template_name': 'create_tile.html'}, name='create_tile'),


####Usage
 
1. To insert image:

        from django.core.files import File
        from thumblr.models import ImageSize
        from thumblr.dto import ImageMetadata
        from thumblr.usecases import add_image
        
        image = File(open('boots.jpg'))
        image_metadata = ImageMetadata(
                file_name='boots.jpg',
                site_id=3,
                size_slug=ImageSize.ORIGINAL,
                content_type_id=5,
                object_id=11,
            )
        add_image(image, image_metadata)
        
2. To use the image into template use template tags:

        {% load thumblr_tags %}
        {% thumblr 'boots.jpg' size='original' %}
        
    In case if site_id, content_type_id, object_id is in template context
    
        {% thumblr_imgs size='original' as imgs %}
        {% for img_url in imgs %}
            {{ img_url }}
        {% endfor %}
        
    It's also possible to use size, site_id, content_type_id, object_id as an additional argument
    
        {% thumblr_imgs size='original' site_id=1 content_type_id=8 object_id=443 as imgs %}
        {% for img_url in imgs %}
            {{ img_url }}
        {% endfor %}
        
    