from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from janrain.capture import Api, ApiResponseError
from janrain.django.capture import get_attribute_map, get_entity_type
from janrain.django.models import CaptureUser

"""
Update Capture User

When a User record is updated the corresponding fields are also updated in the
Capture record.
"""
@receiver(post_save, sender=User)
def update_capture_user(sender, **kwargs):
    # Not necessary to update Capture on create since Capture provides the data
    # initially in the authentication backend.
    if not kwargs['created']:
        user = kwargs['instance']
        try:
            capture_user = CaptureUser.objects.get(user=user)
        except CaptureUser.DoesNotExist:
            return

        attribute_map = get_attribute_map()
        attributes = {}

        for user_attr, entity_attr in attribute_map.items():
            attributes[entity_attr] = getattr(user, user_attr)

        # Use client_id and client_secret since this update may be initiated by
        # a Django administrator.
        api = Api(settings.JANRAIN_CAPTURE['server'])
        response = api.call("/entity.update", type_name=get_entity_type(),
                            uuid=capture_user.uuid,
                            client_id=settings.JANRAIN_CAPTURE['client_id'],
                            client_secret=settings.JANRAIN_CAPTURE['client_secret'],
                            value=attributes)

