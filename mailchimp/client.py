import json
import requests
import hashlib
from mailchimp.enumerator import ErrorEnum
from mailchimp import exception
from requests.auth import HTTPBasicAuth
from mailchimp.clientoauth import ClientOauth


class Client(object):
    def __init__(self, user=None, apikey=None, access_token=None):
        if access_token:
            self.access_token = access_token
            c = ClientOauth(self.access_token)
            self.auth = c
            self.base_url = c.get_base_url() + '/3.0/'
        elif user and apikey:
            self.auth = HTTPBasicAuth(user, apikey)
            self.base_url = 'https://{0}.api.mailchimp.com/3.0/'.format(apikey.split('-').pop())
        else:
            raise exception.CredentialRequired("You must provide either access_token or a username and api_key")

    def _get(self, endpoint, auth):
        response = requests.get(self.base_url + endpoint, auth=auth)
        #return response.json()
        return self._parse(response).json()

    def _post(self, endpoint, auth, data):
        response = requests.post(self.base_url + endpoint, auth=auth, json=data)
        return self._parse(response).json()

    def _delete(self, endpoint, auth):
        response = requests.delete(self.base_url + endpoint, auth=auth)
        return self._parse(response)
    
    def _put(self, endpoint, auth, data):
        response = requests.put(self.base_url + endpoint, data=data, auth=auth)
        return self._parse(response).json()

    def _parse(self, response):
        if not response.ok:
            data = response.json()
            if ('detail' in data and 'status' in data):
                code = data['status']
                message = data['detail']
                try:
                    error_enum = ErrorEnum(code)
                except Exception:
                    raise exception.UnexpectedError('Error: {}. Message {}'.format(code, message))
                if error_enum == ErrorEnum.BadRequest:
                    raise exception.BadRequest(message)
                if error_enum == ErrorEnum.APIKeyMissing:
                    raise exception.APIKeyMissing(message)
                if error_enum == ErrorEnum.Forbidden:
                    raise exception.Forbidden(message)
                if error_enum == ErrorEnum.ResourceNotFound:
                    raise exception.ResourceNotFound(message)
                if error_enum == ErrorEnum.MethodNotAllowed:
                    raise exception.MethodNotAllowed(message)
                if error_enum == ErrorEnum.ResourceNestingTooDeep:
                    raise exception.ResourceNestingTooDeep(message)
                if error_enum == ErrorEnum.InvalidMethodOverride:
                    raise exception.InvalidMethodOverride(message)
                if error_enum == ErrorEnum.TooManyRequests:
                    raise exception.TooManyRequests(message)
                if error_enum == ErrorEnum.InternalServerError:
                    raise exception.InternalServerError(message)
                if error_enum == ErrorEnum.ComplianceRelated:
                    raise exception.ComplianceRelated(message)
                else:
                    raise exception.BaseError('Error: {}. Message {}'.format(code, message))
            return data
        else:
            return response

    def get_lists(self):
        """
        Get all lists
        :return: A dict with all lists
        """
        endpoint = 'lists/'
        return self._get(endpoint=endpoint, auth=self.auth)

    def get_list(self, list_id):
        """
        Get an specific list

        :param list_id: A string, it is the unique id for the list.

        :return: A dictionary with the parameters of the list

        """
        endpoint = 'lists/{0}'.format(list_id)
        return self._get(endpoint=endpoint, auth=self.auth)

    def create_new_list(self, data):
        """
            Create a new list in your MailChimp account.
            :param data: A dictionary with the parameters
            data = {
                "name": string,
                "contact": object
                {
                    "company": string,
                    "address1": string,
                    "city": string,
                    "state": string,
                    "zip": string,
                    "country": string
                },
                "permission_reminder": string,
                "campaign_defaults": object
                {
                    "from_name": string,
                    "from_email": string,
                    "subject": string,
                    "language": string
                },
                "email_type_option": boolean
                }
            :return: A dictionary with the parameters of the list
        """
        if 'name' not in data:
            raise KeyError('The list must have a name')
        if 'contact' not in data:
            raise KeyError('The list must have a contact')
        if 'company' not in data['contact']:
            raise KeyError('The list contact must have a company')
        if 'address1' not in data['contact']:
            raise KeyError('The list contact must have a address1')
        if 'city' not in data['contact']:
            raise KeyError('The list contact must have a city')
        if 'state' not in data['contact']:
            raise KeyError('The list contact must have a state')
        if 'zip' not in data['contact']:
            raise KeyError('The list contact must have a zip')
        if 'country' not in data['contact']:
            raise KeyError('The list contact must have a country')
        if 'permission_reminder' not in data:
            raise KeyError('The list must have a permission_reminder')
        if 'campaign_defaults' not in data:
            raise KeyError('The list must have a campaign_defaults')
        if 'from_name' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a from_name')
        if 'from_email' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a from_email')
        if 'subject' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a subject')
        if 'language' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a language')
        if 'email_type_option' not in data:
            raise KeyError('The list must have an email_type_option')
        if data['email_type_option'] not in [True, False]:
            raise TypeError('The list email_type_option must be True or False')
        endpoint = 'lists/'
        return self._post(endpoint, auth=self.auth, data=data)

    def remove_lists(self, list_id):
        """
        Remove a list from your MailChimp account. If you delete a list,
        you’ll lose the list history—including subscriber activity,
        unsubscribes, complaints, and bounces. You’ll also lose subscribers’
        email addresses, unless you exported and backed up your list.

        :param list_id: A string, it is the unique id for the list.

        """
        endpoint = 'lists/{0}'.format(list_id)
        return self._delete(endpoint, auth=self.auth)

    def get_list_members(self, list_id):
        """
         Get all members form a list
        :param list_id: A string with id_list.
        :return: A dictionary with all members from a list
        """
        endpoint = "lists/{0}/members/".format(list_id)
        return self._get(endpoint, auth=self.auth)

    def add_new_list_member(self, list_id, data):
        """
        Add a new member to the list.
        :param list_id: A string with id_list.
        :param data: A dictionary of parameters, fields "status" and "email_address" are mandatory
                        data = {
                        "status": string*, (Must be one of 'subscribed', 'unsubscribed', 'cleaned',
                        'pending')
                        "email_address": string*
                        }
        :return: A dictionary with the parameters of the new member
        """
        if 'email_address' not in data:
            raise KeyError('The list member must have an email_address')
        if 'status' not in data:
            raise KeyError('The list member must have a status')
        if data['status'] not in ['subscribed', 'unsubscribed', 'cleaned', 'pending']:
            raise ValueError('The list member status must be one of "subscribed", "unsubscribed", "cleaned", '
                             '"pending"')
        endpoint = "lists/{0}/members/".format(list_id)
        return self._post(endpoint, auth=self.auth, data=data)

    def remove_list_member(self, list_id, email):
        """
        Remove a member from a list
        :param list_id: A string with list id
        :param email: a string with email address
        """
        data = {'status': 'unsubscribed'}
        payload = json.dumps(data)
        email_address = email.lower()
        email_address = hashlib.md5(email_address.encode('utf-8')).hexdigest()
        endpoint = 'lists/{0}/members/{1}'.format(list_id, email_address)
        return self._delete(endpoint, auth=self.auth, data=payload)

    def update_list(self):
        raise NotImplementedError

    def get_information_reports(self):
        raise NotImplementedError

    def get_details_report(self):
        raise NotImplementedError

    def get_recent_list_activity(self):
        raise NotImplementedError

    def get_top_email_clients(self):
        raise NotImplementedError

    def get_list_growth_history(self):
        raise NotImplementedError

    def get_list_growth_history_month(self):
        raise NotImplementedError

    def create_new_interest_category(self):
        raise NotImplementedError

    def get_information_list_categories(self):
        raise NotImplementedError

    def update_category(self):
        raise NotImplementedError

    def get_list_location(self):
        raise NotImplementedError

    def get_information_member_list(self):
        raise NotImplementedError

    def get_information_specific_list_member(self):
        raise NotImplementedError

    def update_list_member(self):
        raise NotImplementedError

    def create_merge_field(self):
        raise NotImplementedError

    def get_merge_fields(self, list_id):
        endpoint = "/lists/{0}/merge-fields".format(list_id)
        return self._get(endpoint, auth=self.auth)

    def get_specific_merge_field(self):
        raise NotImplementedError

    def create_new_segment(self):
        raise NotImplementedError

    def remove_list_members_segment(self):
        raise NotImplementedError

    def get_information_segments(self):
        raise NotImplementedError

    def get_information_segment(self):
        raise NotImplementedError

    def update_segment(self):
        raise NotImplementedError

    def remove_segment(self):
        raise NotImplementedError

    def customize_signup(self):
        raise NotImplementedError

    def get_signup(self):
        raise NotImplementedError

    def create_webhook(self):
        raise NotImplementedError

    def get_webhooks(self):
        raise NotImplementedError

    def get_information_specific_webhook(self):
        raise NotImplementedError

    def update_webhook(self):
        raise NotImplementedError

    def remove_webhook(self):
        raise NotImplementedError
