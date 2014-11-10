#Thumblr

Thumblr is an app that proveds an abstraction to deal images throughout the storefront project. The image below illustates the components involved.  

![](http://s3.amazonaws.com/storefront-dump/upload.png)


The upload interface is interface that accepts files as an input.  
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