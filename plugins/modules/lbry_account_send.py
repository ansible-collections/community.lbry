#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_account_send
short_description: Send the same number of credits to multiple addresses from a specific account (or default account).
description:
  - Send the same number of credits to multiple addresses from a specific account (or default account).
  - This module is not idempotent.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options

options:
  addresses:
    description:
      - Address to send credits to.
    type: list
    elements: str
    required: yes
    aliases:
      - address
  amount:
    description:
      - Amount of credits to send.
      - Note that the total amount sent will be amount * number of addresses.
    type: str
  account_id:
    description:
      - account to fund the send.
      - default account will be used if none specified.
    type: str
  wallet_id:
    description:
      - Restrict operation to specific wallet.
    type: str
  preview:
    description:
      - do not broadcast the transaction.
    type: bool
  blocking:
    description:
      - wait until tx has synced
    type: bool

requirements:
  - requests
'''

EXAMPLES = r'''
  - name: Transfer 2.0 LBC to a new address
    community.lbry.lbry_account_send:
      addresses:
        - address1
      amount: '2.0'

  - name: Transfer 2.0L LBC to each address - 6.0 total
    community.lbry.lbry_account_send:
      addresses:
        - address1
        - address2
        - address3
      amount: '2.0'
'''

RETURN = r'''
msg:
  description: A short message describing what happened.
  type: str
  returned: always
  sample: "A new address was generated"
result:
  description: Return dictionary from lbrynet givign details of the transaction.
  type: dict
  returned: on success
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
        addresses=dict(type='list', elements='str', required=True, aliases=['address']),
        amount=dict(type='str'),
        account_id=dict(type='str'),
        wallet_id=dict(type='str'),
        preview=dict(type='bool'),
        blocking=dict(type='bool')
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
    #  debug = module.params['debug']

    response = None
    changed = False

    try:
        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "account_send",
            "params": {}
        }
        request_params = {}
        for item in ['addresses', 'amount', 'account_id', 'wallet_id', 'preview', 'blocking']:
            payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
        response = lbry_request(url, payload)
        response = lbry_process_request(module, response)
        changed = True
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=changed, **response)


if __name__ == '__main__':
    main()
