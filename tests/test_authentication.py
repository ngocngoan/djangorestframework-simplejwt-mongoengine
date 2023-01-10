from datetime import timedelta
from importlib import reload

from bson.objectid import ObjectId
from django_mongoengine.mongo_auth.managers import get_user_document
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken

from rest_framework_simplejwt_mongoengine import authentication
from rest_framework_simplejwt_mongoengine.models import TokenUser
from rest_framework_simplejwt_mongoengine.settings import api_settings
from rest_framework_simplejwt_mongoengine.tokens import AccessToken, SlidingToken

from .utils import BaseTestCase, override_api_settings

User = get_user_document()
AuthToken = api_settings.AUTH_TOKEN_CLASSES[0]


class TestJWTAuthentication(BaseTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.backend = authentication.JWTAuthentication()

        self.fake_token = b"TokenMcTokenface"
        self.fake_header = b"Bearer " + self.fake_token

    def test_get_header(self):
        # Should return None if no authorization header
        request = self.factory.get("/test-url/")
        self.assertIsNone(self.backend.get_header(request))

        # Should pull correct header off request
        request = self.factory.get("/test-url/", HTTP_AUTHORIZATION=self.fake_header)
        self.assertEqual(self.backend.get_header(request), self.fake_header)

        # Should work for unicode headers
        request = self.factory.get(
            "/test-url/", HTTP_AUTHORIZATION=self.fake_header.decode("utf-8")
        )
        self.assertEqual(self.backend.get_header(request), self.fake_header)

        # Should work with the x_access_token
        with override_api_settings(AUTH_HEADER_NAME="HTTP_X_ACCESS_TOKEN"):
            # Should pull correct header off request when using X_ACCESS_TOKEN
            request = self.factory.get(
                "/test-url/", HTTP_X_ACCESS_TOKEN=self.fake_header
            )
            self.assertEqual(self.backend.get_header(request), self.fake_header)

            # Should work for unicode headers when using
            request = self.factory.get(
                "/test-url/", HTTP_X_ACCESS_TOKEN=self.fake_header.decode("utf-8")
            )
            self.assertEqual(self.backend.get_header(request), self.fake_header)

    def test_get_raw_token(self):
        # Should return None if header lacks correct type keyword
        with override_api_settings(AUTH_HEADER_TYPES="JWT"):
            reload(authentication)
            self.assertIsNone(self.backend.get_raw_token(self.fake_header))
        reload(authentication)

        # Should return None if an empty AUTHORIZATION header is sent
        self.assertIsNone(self.backend.get_raw_token(b""))

        # Should raise error if header is malformed
        with self.assertRaises(AuthenticationFailed):
            self.backend.get_raw_token(b"Bearer one two")

        with self.assertRaises(AuthenticationFailed):
            self.backend.get_raw_token(b"Bearer")

        # Otherwise, should return unvalidated token in header
        self.assertEqual(self.backend.get_raw_token(self.fake_header), self.fake_token)

        # Should return token if header has one of many valid token types
        with override_api_settings(AUTH_HEADER_TYPES=("JWT", "Bearer")):
            reload(authentication)
            self.assertEqual(
                self.backend.get_raw_token(self.fake_header),
                self.fake_token,
            )
        reload(authentication)

    def test_get_validated_token(self):
        # Should raise InvalidToken if token not valid
        token = AuthToken()
        token.set_exp(lifetime=-timedelta(days=1))
        with self.assertRaises(InvalidToken):
            self.backend.get_validated_token(str(token))

        # Otherwise, should return validated token
        token.set_exp()
        self.assertEqual(
            self.backend.get_validated_token(str(token)).payload, token.payload
        )

        # Should not accept tokens not included in AUTH_TOKEN_CLASSES
        sliding_token = SlidingToken()
        with override_api_settings(
            AUTH_TOKEN_CLASSES=(
                "rest_framework_simplejwt_mongoengine.tokens.AccessToken",
            )
        ):
            with self.assertRaises(InvalidToken) as e:
                self.backend.get_validated_token(str(sliding_token))

            messages = e.exception.detail["messages"]
            self.assertEqual(1, len(messages))
            self.assertEqual(
                {
                    "token_class": "AccessToken",
                    "token_type": "access",
                    "message": "Token has wrong type",
                },
                messages[0],
            )

        # Should accept tokens included in AUTH_TOKEN_CLASSES
        access_token = AccessToken()
        sliding_token = SlidingToken()
        with override_api_settings(
            AUTH_TOKEN_CLASSES=(
                "rest_framework_simplejwt_mongoengine.tokens.AccessToken",
                "rest_framework_simplejwt_mongoengine.tokens.SlidingToken",
            )
        ):
            self.backend.get_validated_token(str(access_token))
            self.backend.get_validated_token(str(sliding_token))

    def test_get_user(self):
        payload = {"some_other_id": "foo"}
        object_id = ObjectId()

        # Should raise error if no recognizable user identification
        with self.assertRaises(InvalidToken):
            self.backend.get_user(payload)

        payload[api_settings.USER_ID_CLAIM] = object_id

        # Should raise exception if user not found
        with self.assertRaises(AuthenticationFailed):
            self.backend.get_user(payload)

        u = User.create_user(username="markhamill", password="markhamill")
        u.is_active = False
        u.save()

        payload[api_settings.USER_ID_CLAIM] = getattr(u, api_settings.USER_ID_FIELD)

        # Should raise exception if user is inactive
        with self.assertRaises(AuthenticationFailed):
            self.backend.get_user(payload)

        u.is_active = True
        u.save()

        # Otherwise, should return correct user
        self.assertEqual(self.backend.get_user(payload).id, u.id)


class TestJWTStatelessUserAuthentication(BaseTestCase):
    def setUp(self):
        self.backend = authentication.JWTStatelessUserAuthentication()

    def test_get_user(self):
        payload = {"some_other_id": "foo"}

        # Should raise error if no recognizable user identification
        with self.assertRaises(InvalidToken):
            self.backend.get_user(payload)

        payload[api_settings.USER_ID_CLAIM] = 42

        # Otherwise, should return a token user object
        user = self.backend.get_user(payload)

        self.assertIsInstance(user, TokenUser)
        self.assertEqual(user.id, 42)

    def test_custom_tokenuser(self):
        from django.utils.functional import cached_property

        class BobSaget(TokenUser):
            @cached_property
            def username(self):
                return "bsaget"

        temp = api_settings.TOKEN_USER_CLASS
        api_settings.TOKEN_USER_CLASS = BobSaget

        # Should return a token user object
        payload = {api_settings.USER_ID_CLAIM: 42}
        user = self.backend.get_user(payload)

        self.assertIsInstance(user, api_settings.TOKEN_USER_CLASS)
        self.assertEqual(user.id, 42)
        self.assertEqual(user.username, "bsaget")

        # Restore default TokenUser for future tests
        api_settings.TOKEN_USER_CLASS = temp
