from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^all/$', 'images.views.images'),
	url(r'^albums/$', 'images.views.main'),
	url(r'^album/(?P<pk>\d+)/$', 'images.views.album'),
    url(r'^album/(\d+)/(full|thumbnails|edit)/$', 'images.views.album'),
    url(r'^album/update/$', 'images.views.update'),
	url(r'^image/(\d+)/$', 'images.views.image'),
)


