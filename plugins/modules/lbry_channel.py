#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_channel

short_description: Manage LBRY channels.

description:
  - Manage LBRY channels.
  - Add and update channels.
  - Abandon channels.
  - Channels are abandond by retreiving the claim_id from the matched channel name.

author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"

extends_documentation_fragment:
  - community.lbry.lbry_common_options

options:
  name:
    description:
      - The name of the channel.
    type: str
    required: true
    aliases:
      - channel_name
  state:
    description:
      - The desired state of the channel.
    type: str
    choices:
      - "present"
      - "absent"
    default: "present"
  bid:
    description:
      - amount to back the claim.
    type: str
  title:
    description:
      - title of the publication.
    type: str
  description:
    description:
      - description of the publication.
    type: str
  email:
    description:
      - Email address of the channel owner.
    type: str
  website_url:
    description:
      - website url.
    type: str
  featured:
    description:
      - claim_ids of featured content in channel.
    type: list
    elements: str
  tags:
    description:
      - content tags.
    type: list
    elements: str
  languages:
    description:
      - languages used by the channel, using RFC 5646 format.
    type: list
    elements: str
  locations:
    description:
      - locations of the channel-
      - Consisting of 2 letter `country` code and a `state`, `city` and a postal `code` along with a `latitude` and `longitude`.
    type: list
    elements: dict
  thumbnail_url:
    description:
      - thumbnail url
    type: str
  cover_url:
    description:
      - cover url of image.
    type: str
  account_id:
    description:
      - account to use for holding the transaction
    type: str
  wallet_id:
    description:
      - Restrict operation to specific wallet.
    type: str
  funding_account_ids:
    description:
      - ids of accounts to fund this transaction
    type: list
    elements: str
  debug:
    description:
      - Show additional debug output.
    type: bool
    default: false

requirements:
  - requests
'''

EXAMPLES = r'''
- name: Create a channel
  community.lbry.lbry_channel:
    name: rhys
    state: present

- name: Abandon a channel
  community.lbry.lbry_channnel:
    name: rhys
    state: absent

- name: Create a channel
  community.lbry.lbry_channnel:
    name: koolchannel
    title: "My Kool Channel"
    email: myemail@secret.com
    languages:
      - EN
      - DE
      - FR
    tags:
      - videos
      - news
      - funny
'''

RETURN = r'''
msg:
  description: A brief description of what happened.
  returned: always
  type: str
  sample: "Channel koolchannel created"
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from ansible_collections.community.lbry.plugins.module_utils.lbry_common import (
    lbry_common_argument_spec,
    lbry_request,
    lbry_build_url,
    lbry_add_param_when_not_none,
    lbry_channel_list,
    HAS_REQUESTS,
    REQUESTS_IMP_ERR,
)
import traceback

# ================
# Module execution
#


def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True, aliases=['channel_name']),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        bid=dict(type='str'),
        title=dict(type='str'),
        description=dict(type='str'),
        email=dict(type='str'),
        website_url=dict(type='str'),
        featured=dict(type='list', elements='str'),
        tags=dict(type='list', elements='str'),
        languages=dict(type='list', elements='str'),
        locations=dict(type='list', elements='dict'),
        thumbnail_url=dict(type='str'),
        cover_url=dict(type='str'),
        account_id=dict(type='str'),
        wallet_id=dict(type='str'),
        funding_account_ids=dict(type='list', elements='str'),
        debug=dict(type='bool', default=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    if not HAS_REQUESTS:
        module.fail_json(msg=missing_required_lib('requests'),
                         exception=REQUESTS_IMP_ERR)

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']
    channel_name = module.params['name']
    if channel_name.startswith('@') is False:
        channel_name = "@{0}".format(channel_name)
    state = module.params['state']
    debug = module.params['debug']

    response = {}

    try:
        url = lbry_build_url(protocol, host, port)
        channels = lbry_channel_list(url)
        channel_exists = False
        claim_id = None
        r = {}

        for c in channels:
            if c['name'] == channel_name:
                channel_exists = True
                claim_id = c['claim_id']
        # TODO No ability to update a channel yet
        if state == "present":
            if not channel_exists:
                if not module.check_mode:
                    url = lbry_build_url(protocol, host, port)
                    payload = {
                        "method": "channel_create",
                        "params": {}
                    }
                    request_params = {}
                    for item in ['bid', 'title', 'description', 'email', 'website_url', 'featured',
                                 'tags', 'languages', 'locations', 'thumbnail_url', 'cover_url',
                                 'account_id', 'wallet_id', 'funding_account_ids']:
                        payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
                    payload['params']['name'] = channel_name
                    response = lbry_request(url, payload)
                    if "error" in response or "error" in response['result']:
                        module.fail_json(msg='Error creating lbry channel: {0}'.format(response))
                    r['channel_details'] = response['result']
                changed = True
                r['msg'] = "Channel created"
            else:
                changed = False
                r['msg'] = "Channel already exists"
        elif state == "absent":
            if not channel_exists:
                module.exit_json(changed=False, msg="Channel does not exist")
            else:
                url = lbry_build_url(protocol, host, port)
                payload = {
                    "method": "channel_abandon",
                    "params": {"claim_id": claim_id}
                }
                if not module.check_mode:
                    response = lbry_request(url, payload)
                    if "error" in response or "error" in response['result']:
                        module.fail_json(msg='Error abandoning lbry channel {0}'.format(response))
                    r['channel_details'] = response['result']
                changed = True
                r['msg'] = "Channel abandoned"
    except Exception as e:
        if not debug:
            module.fail_json(msg='Error running module: %s' % to_native(e))
        else:
            module.fail_json(msg='Error running module: {0}, response: {1}, payload {2}'.format(traceback.format_exc(), str(response), str(payload)))

    module.exit_json(changed=changed, **r)


if __name__ == '__main__':
    main()
