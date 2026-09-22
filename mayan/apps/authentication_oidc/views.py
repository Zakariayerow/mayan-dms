from django.conf import settings
from django.contrib import auth
from django.shortcuts import resolve_url
from django.utils.http import url_has_allowed_host_and_scheme

from mozilla_django_oidc.views import (
    OIDCAuthenticationCallbackView, OIDCAuthenticationRequestView
)

from mayan.apps.authentication.exceptions import AuthenticationError

from .literals import (
    HEADER_NAME_LOCATION, SESSION_KEY_RENEWAL_NEXT, SESSION_KEY_STATES,
    SESSION_KEY_UPSTREAM_NEXT, STATE_KEY_NEXT
)
from .utils import store_authorization_destination


class MayanOIDCAuthenticationCallbackView(OIDCAuthenticationCallbackView):
    def get(self, request):
        state = request.GET.get('state')
        state_dict = request.session.get(SESSION_KEY_STATES, {})
        state_data = state_dict.get(state, {})
        code = request.GET.get('code')

        self.next_url = state_data.get(STATE_KEY_NEXT)

        self.authentication_attempt = bool(code and state_data)

        request.session.pop(SESSION_KEY_RENEWAL_NEXT, None)
        request.session.pop(SESSION_KEY_UPSTREAM_NEXT, None)

        return super().get(request=request)

    @property
    def failure_url(self):
        return resolve_url(
            self.get_settings('LOGIN_REDIRECT_URL_FAILURE', settings.LOGIN_URL)
        )

    def login_failure(self):
        self.next_url = None

        user = getattr(self.request, 'user', None)

        if self.authentication_attempt and user and user.is_authenticated:
            auth.logout(self.request)

        return super().login_failure()

    @property
    def success_url(self):
        next_url = getattr(self, 'next_url', None)

        if next_url:
            is_allowed = url_has_allowed_host_and_scheme(
                allowed_hosts={
                    self.request.get_host()
                }, require_https=self.request.is_secure(), url=next_url
            )

            if is_allowed:
                return next_url

        return resolve_url(
            self.get_settings('LOGIN_REDIRECT_URL', '/')
        )


class MayanOIDCAuthenticationRequestView(OIDCAuthenticationRequestView):
    def get(self, request):
        response = super().get(request=request)

        is_stored = store_authorization_destination(
            authorization_url=response[HEADER_NAME_LOCATION],
            destination=request.session.get(SESSION_KEY_UPSTREAM_NEXT),
            request=request
        )

        if not is_stored:
            raise AuthenticationError(
                'Unable to record the authorization attempt in the session.'
            )

        return response
