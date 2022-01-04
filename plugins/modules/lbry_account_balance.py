#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_account_balance
short_description: Return the balance of an account.
description:
  - Return the balance of an account.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
options:
  account_id:
    description:
      - If provided only the balance for this account will be given.
      - Otherwise default account is assumed.
    type: str
    aliases:
      - name
  wallet_id:
    description:
      - wallet file name
    type: str
  confirmations:
    description:
      - Only include transactions with this many confirmed blocks.
    type: int
  debug:
    description:
      - Show additional debug output.
    type: bool
    default: false
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Get balance for an account
  community.lbry.lbry_account_balance:
    account_id: myaccount
  register: result

- name: Wait for the available balance to hit an expected level
  community.lbry.lbry_account_balance:
  register: account
  retries: 99
  delay: 10
  until: "account.balance.available == '200.0'"
'''

RETURN = r'''
balance:
  description: Account balance info.
  returned: always
  type: dict
  sample: {"available": "0.0", "reserved": "0.0", "reserved_subtotals": {"claims": "0.0", "supports": "0.0", "tips": "0.0"}, "total": "0.0"}
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
import traceback


# ================
# Module execution
#

def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        account_id=dict(type='str', aliases=['name']),
        wallet_id=dict(type='str'),
        confirmations=dict(type='int'),
        debug=dict(type='bool', default=False)
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
    debug = module.params['debug']
    result = {}

    try:
        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "account_balance",
            "params": {}
        }
        request_params = {}
        for item in ['account_id', 'wallet_id', 'confirmations']:
            payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
        response = lbry_request(url, payload)
        response = lbry_process_request(module, response)
        result['balance'] = response['result']
    except Exception as e:
        if not debug:
            module.fail_json(msg='Error running module: %s' % to_native(e))
        else:
            module.fail_json(msg='Error running module: {0}, response: {1}'.format(traceback.format_exc(), str(response)))

    module.exit_json(changed=False, **result)


if __name__ == '__main__':
    main()
