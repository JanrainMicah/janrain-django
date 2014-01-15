from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def login_required(view_func):
    """
    Redirect users to 'janrain-sign-in' if they are not authenticated.
    """
    def _janrain_user_required(request, *args, **kwargs):
        if not request.user.is_authenticated():
            # TODO: Configurable URL/named URL pattern
            uri = reverse("janrain-sign-in")
            if '?' in uri:
                uri += '&'
            else:
                uri += '?'
            uri += "next=" + request.get_full_path()
            return HttpResponseRedirect(uri)
        return view_func(request, *args, **kwargs)
    return _janrain_user_required
