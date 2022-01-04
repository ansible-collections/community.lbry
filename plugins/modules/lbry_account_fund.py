#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_account_fund
short_description: Transfer LBC from one account to another.
description:
  - Transfer LBC from one account to another.
  - Transfer some amount (or --everything) to an account from another account (can be the same account).
  - Amounts are interpreted as LBC.
  - THis module is not idempotent.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options

options:
  to_account:
    description:
      - send to this account.
    type: str
  from_account:
    description:
      - spend from this account.
    type: str
  amount:
    description:
      - the amount to transfer lbc.
    type: str
  everything:
    description:
      - transfer everything (excluding claims).
    type: bool
    default: false
  outputs:
    description:
      - split payment across many outputs.
    type: int
    default: 1
  wallet_id:
    description:
      - Restrict operation to specific wallet.
    type: str
  broadcast:
    description:
      - actually broadcast the transaction.
    type: bool
    default: false

requirements:
  - requests
'''

EXAMPLES = r'''
- name: Create a new address for the default account.
  community.lbry.lbry_address_unused:
  register: result

- name: Create a new address using a specific account
  community.lbry.lbry_address_unused:
    account_id: mitfZTqgeHFGKPTPVUVNFV2e6TqiZEN8x3
  register: result

- name: Create a new address using a specific account & wallet
  community.lbry.lbry_address_unused:
    account_id: mitfZTqgeHFGKPTPVUVNFV2e6TqiZEN8x3
    wallet_id: 1ExAmpLe0FaBiTco1NADr3sSV5tsGaMF6hd
  register: result

- name: Parse the resulting address into a variable
  set_fact:
    my_new_address: result.address
'''

RETURN = r'''
address:
  description: An address that can be used to send lbry credits to.
  type: str
  returned: on success
  sample: mnTXc8Neq7uhhQJyXDMPfi99QN54PpusFs
msg:
  description: A short message describing what happened.
  type: str
  returned: always
  sample: "A new address was generated"
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
        to_account=dict(type='str'),
        from_account=dict(type='str'),
        amount=dict(type='str'),
        everything=dict(type='bool', default=False),
        outputs=dict(type='int', default=1),
        wallet_id=dict(type='str'),
        broadcast=dict(type='bool', default=False)
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
            "method": "account_fund",
            "params": {}
        }
        request_params = {}
        for item in ['to_account', 'from_account', 'amount', 'everything', 'outputs', 'wallet_id', 'broadcast']:
            payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
        response = lbry_request(url, payload)
        response = lbry_process_request(module, response)
        changed = True
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=changed, **response)


if __name__ == '__main__':
    main()
