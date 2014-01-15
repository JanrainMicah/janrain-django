from django.contrib.auth.models import User, check_password
from django.conf import settings
from janrain.django.models import CaptureUser
from janrain.django.capture import CaptureApi, CaptureApiError, get_attribute_map

import logging
logger = logging.getLogger(__name__)

class CaptureBackend(object):
    """
    Janrain Capture Authentication Backend
    """
    def authenticate(self, access_token):
        """
        Authenticate

        Authenticate users with an access_token provisioned by the Capture widget.
        If the user does not yet exist in Django then they will be created but will
        not be activated.

        Args:
            access_token - Access token provisioned by the Janrain Capture widget.
        """
        attribute_map = get_attribute_map()
        attributes = ['uuid',] + attribute_map.values()

        try:
            api = CaptureApi()
            entity = api.entity(access_token, attributes)
        except CaptureApiError as error:
            logger.warn(error.message)
            return None

        try:
            user = CaptureUser.objects.get(uuid=entity['uuid']).user

            # Sync user attributes from Capture record at login
            for user_attr, entity_attr in attribute_map.items():
                setattr(user, user_attr, entity[entity_attr])
            user.save()

            return user

        except CaptureUser.DoesNotExist:
            # Create user
            user = User()

            for user_attr, entity_attr in attribute_map.items():
                setattr(user, user_attr, entity[entity_attr])

            user.set_unusable_password()

            user.is_active = getattr(settings, 'JANRAIN_ACTIVATE_NEW_USERS', False)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # Create CaptureUser to link the new User to the Capture UUID
            capture_user = CaptureUser(user=user, uuid=entity['uuid'])
            capture_user.save()

            return user

        return None

    def get_user(self, user_id):
        """ Get a User object based on the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
