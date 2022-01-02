#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_publish
short_description: Create or replace a stream claim at a given name.
description:
  - Create or replace a stream claim at a given name.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
options:
  name:
    description:
      - name of the content (can only consist of a-z A-Z 0-9 and -(dash))
    type: str
    required: yes
  bid:
    description:
      - amount to back the claim.
    type: str
  file_path:
    description:
      - path to file to be associated with name.
    type: str
  file_hash:
    description:
      - hash of file to be associated with stream.
    type: str
  validate_file:
    description:
      - validate that the video container and encodings match common web browser support or that optimization succeeds if specified. FFmpeg is required.
    type: bool
    default: false
  optimize_file:
    description:
      - transcode the video & audio if necessary to ensure common web browser support. FFmpeg is required
    type: bool
    default: false
  fee_currency:
    description:
      - specify fee currency.
    type: str
  fee_amount:
    description:
      - content download fee
    type: float
  fee_address:
    description:
      - address where to send fee payments, will use value from --claim_address if not provided
    type: str
  title:
    description:
      - title of the publication
    type: str
  description:
    description:
      - description of the publication
    type: str
  author:
    description:
      - author of the publication.
      - The usage for this field is not the same as for channels.
      - The author field is used to credit an author who is not the publisher and is not represented by the channel.
      - For example, a pdf file of 'The Odyssey' has an author of 'Homer' but may by published to a channel such as '@classics', or to no channel at all.
    type: str
  tags:
    description:
      - add content tags
    type: list
    elements: str
  languages:
    description:
      - languages used by the channel, using RFC 5646 format
    type: list
    elements: str
  locations:
    description:
      - locations relevant to the stream.
      - Consisting of 2 letter `country` code and a `state`, `city` and a postal `code` along with a `latitude` and `longitude`
    type: list
    elements: dict
  license:
    description:
      - publication license
    type: str
  license_url:
    description:
      - publication license url
    type: str
  thumbnail_url:
    description:
      - thumbnail url
    type: str
  release_time:
    description:
      - original public release of content, seconds since UNIX epoch
    type: int
  width:
    description:
      - image/video width, automatically calculated from media file
    type: int
  height:
    description:
      - image/video width, automatically calculated from media file
    type: int
  duration:
    description:
      - audio/video duration in seconds, automatically calculated
    type: int
  sd_hash:
    description:
      - sd_hash of stream
    type: str
  channel_id:
    description:
      - claim id of the publisher channel
    type: str
  channel_name:
    description:
      - name of publisher channel
    type: str
  channel_account_id:
    description:
      - one or more account ids for accounts to look in for channel certificates, defaults to all accounts.
    type: str
  account_id:
    description:
      - account to use for holding the transaction
    type: str
  wallet_id:
    description:
      - restrict operation to specific wallet
    type: str
  funding_account_ids:
    description:
      - ids of accounts to fund this transaction
    type: str
  claim_address:
    description:
      - address where the claim is sent to, if not specified it will be determined automatically from the account
    type: str
  preview:
    description:
      - do not broadcast the transaction
    type: bool
  blocking:
    description:
      - wait until transaction is in mempool
    type: bool

requirements:
  - requests
'''

EXAMPLES = r'''
- name: Get lbry version info
  community.lbry.lbry_get:
    uri: TODO
    download_directory: /lbry/downloads
  register: result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from ansible_collections.community.lbry.plugins.module_utils.lbry_common import (
    lbry_common_argument_spec,
    lbry_request,
    lbry_build_url,
    lbry_add_param_when_not_none,
    HAS_REQUESTS,
    REQUESTS_IMP_ERR,
    lbry_process_request,
)

# ================
# Module execution
#


def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        bid=dict(type='str'),
        file_path=dict(type='str'),
        file_hash=dict(type='str'),
        validate_file=dict(type='bool', default=False),
        optimize_file=dict(type='bool', default=False),
        fee_currency=dict(type='str'),
        fee_amount=dict(type='float'),
        fee_address=dict(type='str'),
        title=dict(type='str'),
        description=dict(type='str'),
        author=dict(type='str'),
        tags=dict(type='list', elements='str'),
        languages=dict(type='list', elements='str'),
        locations=dict(type='list', elements='dict'),
        license=dict(type='str'),
        license_url=dict(type='str'),
        thumbnail_url=dict(type='str'),
        release_time=dict(type='int'),
        width=dict(type='int'),
        height=dict(type='int'),
        duration=dict(type='int'),
        sd_hash=dict(type='str'),
        channel_id=dict(type='str'),
        channel_name=dict(type='str'),
        channel_account_id=dict(type='str'),
        account_id=dict(type='str'),
        wallet_id=dict(type='str'),
        funding_account_ids=dict(type='str'),
        claim_address=dict(type='str'),
        preview=dict(type='bool'),
        blocking=dict(type='bool'),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )

    if not HAS_REQUESTS:
        module.fail_json(msg=missing_required_lib('requests'),
                         exception=REQUESTS_IMP_ERR)

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']

    response = {}
    changed = False
    msg = None

    url = lbry_build_url(protocol, host, port)
    payload = {
        "method": "publish",
        "params": {}
    }
    request_params = {}
    for item in module.params:
        if item not in ['host', 'port', 'protocol', 'debug']:
            payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
    try:
        lbry_process_request(module, url, payload)
    except Exception as excep:
        if module.params['debug']:
            module.fail_json(msg='Error publishing file to lbrynet: {0}'.format(response))
        else:
            module.fail_json(msg="Error publishing file to lbrynet")


if __name__ == '__main__':
    main()
