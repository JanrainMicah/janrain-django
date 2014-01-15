from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.core.exceptions import ImproperlyConfigured
from janrain.django.capture import CaptureApi, CaptureApiError
from janrain.django.session import set_session

import logging
logger = logging.getLogger(__name__)

def sign_in(request):
    # The same redirect URI needs to be set in the Javascript settings for
    # Capture as well as passed to the oauth/token API call.
    query_start = request.build_absolute_uri().find('?')
    redirect_uri = request.build_absolute_uri()[0:query_start].strip('/')

    # Store the next URL in the session so that we don't have to pass it around
    # through the Capture redirects.
    if 'next' in request.GET:
        request.session['next'] = request.GET['next']

    context = {'redirect_uri': redirect_uri}

    if 'code' in request.GET:
        # Exchange the code for access and refresh tokens.
        api = CaptureApi()
        try:
            api_response = api.oauth_token(request.GET['code'], redirect_uri)
        except CaptureApiError as error:
            logger.warn(str(error))
            messages.error(request, "Error: " + str(error))
            return redirect('janrain-sign-in')

        user = authenticate(access_token=api_response['access_token'])

        if not user:
            # Yes, it's not a very helpful error message but it's an edge case
            messages.error(request, "Authentication failed.")
            return redirect('janrain-sign-in')

        if user.is_active:
            login(request, user)
            set_session(request.session, api_response)

            if 'next' in request.session:
                next = request.session['next']
                del request.session['next']
                return redirect(next)
            elif hasattr(settings, 'JANRAIN_SIGN_IN_REDIRECT'):
                return redirect(settings.JANRAIN_SIGN_IN_REDIRECT)
        else:
            messages.error(request, "That account has not been activated.")
            return redirect('janrain-sign-in')

    return render(request, "janrain/sign-in.html", context)

def sign_out(request):
    logout(request)

    if hasattr(settings, 'JANRAIN_SIGN_OUT_REDIRECT'):
        return redirect(settings.JANRAIN_SIGN_OUT_REDIRECT)

    return render(request, "janrain/sign-out.html", {})


