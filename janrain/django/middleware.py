from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.template import loader
from django.conf import settings
from django.contrib.auth import logout
from datetime import datetime
from janrain.django.session import refresh_session

import logging
logger = logging.getLogger(__name__)

class RefreshTokenMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and self.token_is_expired(request):
            try:
                logger.debug("Refreshing Capture access token")
                refresh_session(request.session)
            except Exception as error:
                logger.warn(str(error))
                logout(request)

        return None

    def token_is_expired(self, request):
        if 'janrain_expires' in request.session:
            return datetime.now() >= request.session['janrain_expires']

