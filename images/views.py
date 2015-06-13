from .models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
from collections import defaultdict
from django.template import RequestContext
from string import join
# Create your views here.

def main(request):
    albums = Album.objects.all()
    if not request.user.is_authenticated():
        albums = albums.filter(public=True)

    paginator = Paginator(albums,10)
    try:
        page = int(request.GET.get("page","1"))
    except ValueError:
        page = 1
    try:
        albums = paginator.page(page)
    except (InvalidPage, EmptyPage):
        albums = paginator.page(paginator.num_pages)


    for album in albums.object_list:
        album.images = album.image_set.all()[:6]

    return render_to_response("list.html", dict(albums=albums, user=request.user, media_url=MEDIA_URL))


def album(request,pk, view ="thumbnails"):
    album = Album.objects.get(pk=pk)
    if not album.public and not request.user.is_authenticated():
        return HttpResponse("Error : You should be logged in to view this album")

    images = album.image_set.all()
    paginator = Paginator(images, 5)
    try:
        page = request.GET.get("page", "1")
    except ValueError:
        page =1
    try:
        images = paginator.page(page)
    except (InvalidPage, EmptyPage):
        images = paginator.page(paginator.num_pages)

     # add list of tags as string and list of album names to each image object
    for img in images.object_list:
        tags = [x[1] for x in img.tags.values_list()]
        img.tag_lst = join(tags, ', ')
        img.album_lst = [x[1] for x in img.albums.values_list()]


    d = dict(album=album, images=images, user = request.user, media_url = MEDIA_URL, view=view, albums=Album.objects.all() )
    d.update(csrf(request))
    return render_to_response('album.html',d )

'''
def update(*args):
    print args
'''


def update(request):
    """Update image title, rating, tags, albums ."""
    p = request.POST
    images = defaultdict(dict)

    #create dictionary of properties for each image

    for k, v in p.items():
        if k.startswith("title") or k.startswith("rating") or k.startswith("tags"):
            k, pk = k.split('-')
            images[pk][k] = v
        elif k.startswith("album"):
            pk = k.split('-')[1]
            images[pk]["albums"] = p.getlist(k)

    for k, d in images.items():
        image = Image.objects.get(pk=k)
        image.title = d['title']
        image.rating =int(d['rating'])

        #tags - assign or create if a new tag!

        tags = d["tags"].split(', ')
        lst = []
        for t in tags:
            if t:
                lst.append(Tag.objects.get_or_create(tag=t)[0])
        image.tags = lst

        if "albums" in d:
            image.albums = d["albums"]
        image.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"], dict(media_url = MEDIA_URL))




def image(request, pk):
    return render_to_response("image.html",dict(image=Image.objects.get(pk=pk), backurl=request.META["HTTP_REFERER"], media_url=MEDIA_URL ) )






def images(request):
    return render_to_response('images.html','')

