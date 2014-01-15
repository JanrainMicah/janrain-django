from django.conf import settings
from janrain.capture import Api, ApiResponseError

import logging
logger = logging.getLogger(__name__)

# Make sure the required JANRAIN_CAPTURE setting is defined
if not hasattr(settings, 'JANRAIN_CAPTURE'):
    raise ImproperlyConfigured("You need to specify JANRAIN_CAPTURE in " \
                               "your Django settings file.")

class CaptureApiError(ApiResponseError):
    pass

class CaptureApi(Api):
    def __init__(self):
        super(CaptureApi, self).__init__(settings.JANRAIN_CAPTURE['server'])
        self.logger = logger

    def call(self, api_call, **kwargs):
        # wrap the call method so we can raise a local exception instead
        try:
            return super(CaptureApi, self).call(api_call, **kwargs)
        except ApiResponseError as error:
            raise CaptureApiError(error.code, error.error, str(error), error.response)

    def entity(self, access_token, attributes=None):
        """
        Get the entity scoped to the specified access_token.

        Args:
            access_token - A Capture access token
            attributes   - A list of attributes to include in response

        Returns:
            The entity as a dictionary
        """
        kwargs = {
            'type_name': get_entity_type(),
            'access_token': access_token
        }

        if attributes:
            kwargs['attributes'] = attributes

        response = self.call("/entity", **kwargs)

        return response['result']

    def oauth_token(self, code, redirect_uri):
        self.sign_requests = False
        response = self.call("/oauth/token", code=code,
                            client_id=settings.JANRAIN_CAPTURE['client_id'],
                            client_secret=settings.JANRAIN_CAPTURE['client_secret'],
                            grant_type='authorization_code',
                            redirect_uri=redirect_uri)
        logger.debug(response)

        return response

    def oauth_refresh_token(self, refresh_token):
        """
        Call /oauth/token to refresh the current token.

        Args:
            refresh_token - The current refresh token, typically saved in the session.

        Returns:
            The API response as a dictionary
        """
        self.sign_requests = False
        response = self.call("/oauth/token",
                             refresh_token=refresh_token,
                             client_id=settings.JANRAIN_CAPTURE['client_id'],
                             client_secret=settings.JANRAIN_CAPTURE['client_secret'],
                             grant_type='refresh_token')
        logger.debug(response)

        return response

def get_attribute_map():
    """
    Return the mapping from Django's User object fields to Capture attributes.
    """
    default_map = {
        'username': 'displayName',
        'email': 'email',
        'first_name': 'givenName',
        'last_name': 'familyName'
    }

    return getattr(settings, 'JANRAIN_CAPTURE_ATTRIBUTE_MAP', default_map)

def get_entity_type():
    """
    Return the entity type (aka. type name) for Capture.
    """

    return getattr(settings, 'JANRAIN_CAPTURE_ENTITY_TYPE', "user")

