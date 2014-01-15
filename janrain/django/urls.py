from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

urlpatterns = patterns('janrain.django.views',
    url(r'^sign-in/$', 'sign_in', name='janrain-sign-in'),
    url(r'^sign-out/$', 'sign_out', name='janrain-sign-out'),
)
