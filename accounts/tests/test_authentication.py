from unittest.mock import Mock, patch
from django.test import TestCase

from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)

mock_post = Mock()
@patch('accounts.authentication.requests.post', mock_post)
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        self.mock_response = mock_post.return_value
        self.mock_response.ok = True

    def tearDown(self):
        mock_post.reset_mock()


    def test_sends_assertion_to_mozilla_with_domain(self):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': DOMAIN}
        )


    def test_return_none_if_response_errors(self):
        self.mock_response.ok = False
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)


    def test_returns_none_if_status_not_okay(self):
        self.mock_response.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)
