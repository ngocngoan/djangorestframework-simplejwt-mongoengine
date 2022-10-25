from unittest.mock import patch

from django.core.management import call_command
from django_mongoengine.mongo_auth.managers import get_user_document
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.utils import aware_utcnow, datetime_from_epoch

from rest_framework_simplejwt_mongoengine.settings import api_settings
from rest_framework_simplejwt_mongoengine.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt_mongoengine.tokens import (
    AccessToken,
    RefreshToken,
    SlidingToken,
)

from .utils import BaseTestCase

User = get_user_document()


class TestTokenBlacklist(BaseTestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="test_password",
        )

    def test_sliding_tokens_are_added_to_outstanding_list(self):
        token = SlidingToken.for_user(self.user)

        qs = OutstandingToken.objects.all()
        outstanding_token = qs.first()

        self.assertEqual(qs.count(), 1)
        self.assertEqual(outstanding_token.user, self.user)
        self.assertEqual(outstanding_token.jti, token["jti"])
        self.assertEqual(outstanding_token.token, str(token))
        self.assertEqual(outstanding_token.created_at, token.current_time)
        self.assertEqual(
            outstanding_token.expires_at, datetime_from_epoch(token["exp"])
        )

    def test_refresh_tokens_are_added_to_outstanding_list(self):
        token = RefreshToken.for_user(self.user)

        qs = OutstandingToken.objects.all()
        outstanding_token = qs.first()

        self.assertEqual(qs.count(), 1)
        self.assertEqual(outstanding_token.user, self.user)
        self.assertEqual(outstanding_token.jti, token["jti"])
        self.assertEqual(outstanding_token.token, str(token))
        self.assertEqual(outstanding_token.created_at, token.current_time)
        self.assertEqual(
            outstanding_token.expires_at, datetime_from_epoch(token["exp"])
        )

    def test_access_tokens_are_not_added_to_outstanding_list(self):
        AccessToken.for_user(self.user)

        qs = OutstandingToken.objects.all()

        self.assertFalse(qs.exists())

    def test_token_will_not_validate_if_blacklisted(self):
        token = RefreshToken.for_user(self.user)
        outstanding_token = OutstandingToken.objects.first()

        # Should raise no exception
        RefreshToken(str(token))

        # Add token to blacklist
        BlacklistedToken.objects.create(token=outstanding_token)

        with self.assertRaises(TokenError) as e:
            # Should raise exception
            RefreshToken(str(token))
            self.assertIn("blacklisted", e.exception.args[0])

    def test_tokens_can_be_manually_blacklisted(self):
        token = RefreshToken.for_user(self.user)

        # Should raise no exception
        RefreshToken(str(token))

        self.assertEqual(OutstandingToken.objects.count(), 1)

        # Add token to blacklist
        blacklisted_token = token.blacklist()

        # Should not add token to outstanding list if already present
        self.assertEqual(OutstandingToken.objects.count(), 1)

        # Should return blacklist record and boolean to indicate creation
        self.assertEqual(blacklisted_token.token.jti, token["jti"])

        with self.assertRaises(TokenError) as e:
            # Should raise exception
            RefreshToken(str(token))
            self.assertIn("blacklisted", e.exception.args[0])

        # If blacklisted token already exists, indicate no creation through
        # boolean
        blacklisted_token = token.blacklist()
        self.assertEqual(blacklisted_token.token.jti, token["jti"])

        # Should add token to outstanding list if not already present
        new_token = RefreshToken()
        blacklisted_token = new_token.blacklist()
        self.assertEqual(blacklisted_token.token.jti, new_token["jti"])

        self.assertEqual(OutstandingToken.objects.count(), 2)


class TestTokenBlacklistFlushExpiredTokens(BaseTestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            password="test_password",
        )

    def test_it_should_delete_any_expired_tokens(self):
        # Make some tokens that won't expire soon
        not_expired_1 = RefreshToken.for_user(self.user)
        not_expired_2 = RefreshToken.for_user(self.user)
        not_expired_3 = RefreshToken()

        # Blacklist fresh tokens
        not_expired_2.blacklist()
        not_expired_3.blacklist()

        # Make tokens with fake exp time that will expire soon
        fake_now = aware_utcnow() - api_settings.REFRESH_TOKEN_LIFETIME

        with patch(
            "rest_framework_simplejwt_mongoengine.tokens.aware_utcnow"
        ) as fake_aware_utcnow:
            fake_aware_utcnow.return_value = fake_now
            expired_1 = RefreshToken.for_user(self.user)
            expired_2 = RefreshToken()

        # Blacklist expired tokens
        expired_1.blacklist()
        expired_2.blacklist()

        # Make another token that won't expire soon
        not_expired_4 = RefreshToken.for_user(self.user)

        # Should be certain number of outstanding tokens and blacklisted
        # tokens
        self.assertEqual(OutstandingToken.objects.count(), 6)
        self.assertEqual(BlacklistedToken.objects.count(), 4)

        call_command("flushexpiredtokens")

        # Expired outstanding *and* blacklisted tokens should be gone
        self.assertEqual(OutstandingToken.objects.count(), 4)
        self.assertEqual(BlacklistedToken.objects.count(), 2)

        self.assertEqual(
            [i.jti for i in OutstandingToken.objects.order_by("id")],
            [
                not_expired_1["jti"],
                not_expired_2["jti"],
                not_expired_3["jti"],
                not_expired_4["jti"],
            ],
        )
        self.assertEqual(
            [i.token.jti for i in BlacklistedToken.objects.order_by("id")],
            [not_expired_2["jti"], not_expired_3["jti"]],
        )

    def test_token_blacklist_will_not_be_removed_on_User_delete(self):
        token = RefreshToken.for_user(self.user)
        outstanding_token = OutstandingToken.objects.first()

        # Should raise no exception
        RefreshToken(str(token))

        # Add token to blacklist
        BlacklistedToken.objects.create(token=outstanding_token)

        with self.assertRaises(TokenError) as e:
            # Should raise exception
            RefreshToken(str(token))
            self.assertIn("blacklisted", e.exception.args[0])

        # Delete the User and try again
        self.user.delete()

        with self.assertRaises(TokenError) as e:
            # Should raise exception
            RefreshToken(str(token))
            self.assertIn("blacklisted", e.exception.args[0])
