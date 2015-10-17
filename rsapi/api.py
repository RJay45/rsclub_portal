from .models import ApiKey
from urllib import request, error
import json


class Api:
    def __init__(self):
        self.key = None
        self._check_key()
        print(self.key)

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

        # Create base API call with authentication data
        call = self.key.url + command + "?auth-userid=" + self.key.userId + "&api-key=" + self.key.authKey

        # Add additional parameters
        if kv_pairs is not None and isinstance(kv_pairs, dict):
            for item in kv_pairs.items():
                if not isinstance(item[0], str):
                    continue

                if isinstance(item[1], str):
                    call += "&" + item[0] + "=" + item[1]
                elif isinstance(item[1], tuple) or isinstance(item[1], list):
                    for sub_item in item[1]:
                        call += "&" + item[0] + "=" + sub_item

        print(call)
        return_value = None

        try:
            api_call = request.Request(call)
            return_value = json.loads(request.urlopen(api_call).read().decode('utf-8'))
        except error.HTTPError as e:
            print("Error - HTTP code " + str(e.code) + " response: " + str(e))
        except error.URLError as e:
            print("Error - There was a problem with the request: " + str(e))
        except Exception as e:
            print("Unknown error was caught: " + str(e))
        else:
            # Update the last success on the key so that it is tried first next time.
            self.key.lastSuccess = ApiKey.get_now()
            self.key.save()
        finally:
            return return_value

    def check_domain_availability(self, domain_name, tlds=None):
        if not isinstance(domain_name, str) and not isinstance(domain_name, tuple) and not isinstance(domain_name, list):
            return None
        if not isinstance(tlds, str) and not isinstance(tlds, tuple) and not isinstance(tlds, list):
            return None

        result = self._api_call('domains/available.json', {'domain-name': domain_name, 'tlds': tlds})

        return result





