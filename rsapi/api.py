__author__ = 'jason'

from .models import ApiKey
from urllib import request, error
import json


class Api:
    def __init__(self):
        self.key = None
        self._check_key()
        print(self.key)
        data = self._api_call('domains/available.json', {'domain-name':'google', 'tlds':'com'})
        print(data)

    def _check_key(self):
        if self.key is None or not self.key.is_valid():
            for key in ApiKey.get_valid():
                self.key = key
                if self._check_connection():
                    break
                else:
                    self.key = None

        if self.key is None:
            print("No valid key found!")
            return False

        return True

    def _check_connection(self):
        return self.key is not None \
            and self._api_call('domains/available.json', {'domain-name':'google', 'tlds':'com'}) is not None

    def _api_call(self, command, kv_pairs=None):
        if self.key is None:
            raise Exception("No API key available. Unable to make API call.")

        if command is None or not isinstance(command, str):
            raise Exception("An API command must be specified")

        #Create base API call with authentication data
        call = self.key.url + command + "?auth-userid=" + self.key.userId + "&api-key=" + self.key.authKey

        #Add additional parameters
        if kv_pairs is not None and isinstance(kv_pairs, dict):
            for item in kv_pairs.items():
                call += "&" + item[0] + "=" + item[1]

        print(call)

        try:
            apicall = request.Request(call)
            return json.loads(request.urlopen(apicall).read().decode('utf-8'))
        except error.HTTPError as e:
            print("Error - HTTP code " + str(e.code) + " response: " + e.reason)
            return None