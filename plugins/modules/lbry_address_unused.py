#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_address_unused
short_description: Return an address containing no balance.
description:
  - Return an address containing no balance.
  - Will create a new address if there is none.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options

options:
  account_id:
    description:
      - account to use for holding the transaction
    type: str
  wallet_id:
    description:
      - Restrict operation to specific wallet.
    type: str

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
)

# ================
# Module execution
#


def main():
    argument_spec = lbry_common_argument_spec()
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )
    argument_spec.update(
        account_id=dict(type='str'),
        wallet_id=dict(type='str'),
    )

    if not HAS_REQUESTS:
        module.fail_json(msg=missing_required_lib('requests'),
                         exception=REQUESTS_IMP_ERR)

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']
    account_id = module.params['account_id']
    wallet_id = module.params['wallet_id']

    result = {}

    try:
        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "address_unused",
            "params": {}
        }
        request_params = {}
        for item in ['account_id', 'wallet_id']:
            payload['params'] = lbry_add_param_when_not_none(request_params, module, item)  
        response = lbry_request(url, payload)
        if 'result' in response:
            result['address'] = response['result']
            result['msg'] = "A new address was generated"
            result['changed'] = True
        elif 'error' in response:
            module.fail_json(msg=response['message'])
        else:
            module.fail_json(msg="Something went badly wrong: {0}".format(response))
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=False, **result)


if __name__ == '__main__':
    main()
