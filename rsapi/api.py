from .models import ApiKey
from urllib import request, error
from enum import Enum
import json


class _ApiEnum(Enum):
    def __str__(self):
        return self.name

########################################################################################################################


class InvoiceMode(_ApiEnum):
    NoInvoice = "NoInvoice"
    PayInvoice = "PayInvoice"
    KeepInvoice = "KeepInvoice"

########################################################################################################################


class PrivacyEnabled(_ApiEnum):
    Yes = "true"
    No = "false"
    Na = "na"

########################################################################################################################


class DomainStatus(_ApiEnum):
    InActive = "InActive"
    Active = "Active"
    Suspended = "Suspended"
    PendingDeleteRestorable = "Pending Delete Restorable"
    Deleted = "Deleted"
    Archived = "Archived"
    PendingVerification = "Pending Verification"
    FailedVerification = "Failed Verification"


########################################################################################################################


class OrderBy(_ApiEnum):
    OrderId = "orderid"
    CustomerId = "customerid"
    EndTime = "endtime"
    Timestamp = "timestamp"
    EntityTypeId = "entityypeid"
    CreationTime = "creationtime"
    CreationDate = "creationdt"


########################################################################################################################


class ApiException(Exception):
    def __init__(self, message, is_connection=False, request_str=None, response_str=None, origin_exception=None):
        self.message = message
        self.request = request_str
        self.response = response_str
        self.origin_exception = origin_exception

        if not isinstance(is_connection, bool):
            is_connection = False

        self.is_connection = is_connection

    def __str__(self):
        return "API Exception: " + self.message + "\nRequest: " + self.request + "\nResponse: " + self.response +\
               "\nOrigin Exception: " + str(self.origin_exception)

########################################################################################################################


class Api:
    def __init__(self):
        self.key = None
        self._load_key()

    def _load_key(self):
        if self.key is None or not self.key.is_valid():
            for key in ApiKey.get_valid():
                self.key = key
                if self._check_connection():
                    break
                else:
                    self.key = None

    def _check_connection(self):
        return self.key is not None \
            and self._api_call('domains/available.json', {'domain-name': 'google', 'tlds': 'com'}) is not None

    @staticmethod
    def _is_compatible_object(obj):
        return isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, bool) or isinstance(obj, _ApiEnum)

    def _api_call(self, command, kv_pairs=None):
        if self.key is None:
            raise ApiException("No API key available. Unable to make API call.", True)

        if command is None or not isinstance(command, str):
            raise ValueError("An API command must be specified")

        # Create base API call with authentication data
        call = self.key.url + command + "?auth-userid=" + self.key.userId + "&api-key=" + self.key.authKey

        # Add additional parameters - skip anything invalid
        if kv_pairs is not None and isinstance(kv_pairs, dict):
            for item in kv_pairs.items():
                if not isinstance(item[0], str):
                    continue

                if Api._is_compatible_object(item[1]):
                    call += "&" + item[0] + "=" + str(item[1])
                elif isinstance(item[1], tuple) or isinstance(item[1], list):
                    for sub_item in item[1]:
                        if Api._is_compatible_object(sub_item):
                            call += "&" + item[0] + "=" + str(sub_item)

        print(call)
        response = None
        return_value = None

        try:
            try:
                api_call = request.Request(call)
                response = request.urlopen(api_call).read().decode('utf-8')
                return_value = json.loads(response)
            except error.HTTPError as e:
                print(e)
                if e.getcode() == 500:
                    # We want to read HTTP 500 errors as JSON, but let's check it's what we think it it
                    response = e.read().decode('utf-8')
                    return_value = json.loads(response)

                    if not isinstance(return_value, dict):
                        raise ApiException("An HTTP code " + str(e.getcode()) + " was received.",
                                           True, call, response, e)
                    else:
                        # Update the last success on the key so that it is tried first next time.
                        self.key.update_last_valid()
                        raise ApiException(return_value.get('message'), False, call, response)
                else:
                    raise ApiException("An HTTP code " + str(e.getcode()) + " was received.",
                                       True, call, response, e)
            except error.URLError as e:
                raise ApiException("There was a problem making the request.", True, call, None, e)

            else:
                # Update the last success on the key so that it is tried first next time.
                self.key.update_last_valid()
        except ValueError as e:
            raise ApiException("An invalid JSON response was received.", True, call, return_value, e)
        except ApiException as e:
            raise e

        return return_value

    """
        See API guide: http://manage.india.resellerclub.com/kb/answer/764
    """
    def domain_check_availability(self, domain_name, tlds=None):
        if (not isinstance(domain_name, str) and not isinstance(domain_name, tuple) and
                not isinstance(domain_name, list) and not isinstance(tlds, str) and
                not isinstance(tlds, tuple) and not isinstance(tlds, list)):
            ValueError("Invalid value specified for API call.")

        return self._api_call('domains/available.json', {'domain-name': domain_name, 'tlds': tlds})

    """
        See API guide: http://manage.india.resellerclub.com/kb/answer/771
    """
    def domain_order_search(self, per_page, page, **kwargs):
        if not isinstance(per_page, int) or not isinstance(page, int) or per_page < 10 or per_page > 500:
            raise ValueError("Invalid page attributes. Values must be integer and per page must be between 10 and 500.")

        options = {
            'order_by': (OrderBy, list, tuple),
            'order_id': (int, list, tuple),
            'reseller_id': (int, list, tuple),
            'customer_id': (int, list, tuple),
            'show_child_orders': (bool, ),
            'product_key': (str, list, tuple),
            'status': (DomainStatus, list, tuple),
            'domain_name': (str, list, tuple),
            'privacy_enabled': (PrivacyEnabled,),
            'creation_date_start': (str, int),
            'creation_date_end': (str, int),
            'expiry_date_start': (str, int),
            'expiry_date_end': (str, int)
        }
        arguments = {'page-no': page, 'no-of-records': per_page}

        for kw in kwargs:
            if options.get(kw):
                for otype in options.get(kw):
                    if isinstance(kwargs.get(kw), otype):
                        arguments[kw.replace('_', '-')] = kwargs.get(kw)
                        break

        return self._api_call('domains/search.json', arguments)

    """
        See API guide: http://manage.india.resellerclub.com/kb/answer/752
    """
    def domain_register(self, domain_name, years, ns, customer_id, contact_id, reg_contact_id,
                        admin_contact_id, tech_contact_id, billing_contact_id, invoice_mode):

        if (not isinstance(domain_name, str) or
                not isinstance(years, int) or
                not (isinstance(ns, str) or isinstance(ns, list) or isinstance(ns, tuple)) or
                not isinstance(customer_id, int) or
                not isinstance(contact_id, int) or
                not isinstance(reg_contact_id, int) or
                not isinstance(admin_contact_id, int) or
                not isinstance(tech_contact_id, int) or
                not isinstance(billing_contact_id, int) or
                not isinstance(invoice_mode, InvoiceMode)):
            raise ValueError("Invalid value specified for API call.")

        return self._api_call('domains/register.json', {'domain-name': domain_name,
                                                        'years': years,
                                                        'ns': ns,
                                                        'customer-id': customer_id,
                                                        'contact-id': contact_id,
                                                        'admin-contact-id': admin_contact_id,
                                                        'reg-contact-id': reg_contact_id,
                                                        'tech-contact-id': tech_contact_id,
                                                        'billing-contact-id': billing_contact_id,
                                                        'invoice-option': invoice_mode
                                                        })

