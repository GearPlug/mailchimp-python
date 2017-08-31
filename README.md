# mailchimp-python

Mailchimp is a lightweight wrapper over MailchimpAPI

## Installing
```
  pip install git+git:https://github.com/GearPlug/mailchimp-python.git
```

## Usage

There are two forms of starting. 

With access_token, you need register your app. You should be able to find the access token according with the documentation https://developer.mailchimp.com/documentation/mailchimp/guides/how-to-use-oauth2/ 

```
from mailchimp.client import Client
client=Client(access_token="Your ACCESS_TOKEN")
```

With credentials, get your APIKEY from your mailchimp account (Account > Extra > Api Keys). USER is the one you use to login.

```
from mailchimp.client import Client
client=Client(user="Your USER", apikey="Your APIKEY")
```

Get all lists

```
client.get_lists()
```
Get an specific list

```
client.get_list('list_id')
```
Add a new list member
```
client.add_new_list_member('list_id',{"email_address":"EMAIL", "status":"subscribed"}))
```

## Requirements

- requests
- hashlib


## Tests

```
python tests/test_client.py

```
## TODO

- update_list
- get_information_reports
- get_details_report
- get_recent_list_activity
- get_top_email_clients
- get_list_growth_history
- get_list_growth_history_month
- create_new_interest_category
- get_information_list_categories
- update_category
- get_list_location
- get_information_member_list
- get_information_specific_list_member
- update_list_member
- create_merge_field
- get_merge_fields
- get_specific_merge_field
- create_new_segment
- remove_list_members_segment
- get_information_segments
- get_information_segment
- update_segment
- remove_segment
- customize_signup
- get_signup
- create_webhook
- get_webhooks
- get_information_specific_webhook
- update_webhook
- remove_webhook