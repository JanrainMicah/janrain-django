from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from datetime import datetime, timedelta
from janrain.django.capture import CaptureApi, CaptureApiError

def set_session(session, api_response):
    # Save new tokens in the session
    session['janrain_access_token'] = api_response['access_token']
    session['janrain_refresh_token'] = api_response['refresh_token']
    expires = datetime.now() + timedelta(0, api_response['expires_in'])
    session['janrain_expires'] = expires

def refresh_session(session):
    # Refresh the token
    api = CaptureApi()
    token = session['janrain_refresh_token']
    api_response = api.oauth_refresh_token(token)

    set_session(session, api_response)
