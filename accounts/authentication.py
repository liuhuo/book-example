__author__ = 'liuhuo'

import requests
import sys
from accounts.models import ListUser

class PersonaAuthenticationBackend(object):
    def authentication(self, assertion):
        data = {'assertion': assertion, 'audience': 'localhost'}
        print('sending to mozilla', data, file=sys.stderr)
        resp = requests.post('https://verifier.login.persona.org/verify', data=data)
        print('got', resp.content, file=sys.stderr)

        if resp.ok:
            verification_data = resp.json()
            if verification_data['status'] == 'okey':
                email = verification_data['email']
                try:
                    return self.get_user(email)
                except ListUser.DoesNotExist:
                    return ListUser.objects.create(email=email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)