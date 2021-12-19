#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_wallet_balance
short_description: Return the balance of a wallet.
description:
  - Return the balance of a wallet.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
options:
  wallet_id:
    description:
      - wallet file name
    type: str
    required: yes
  debug:
    description:
      - Show additional debug output.
    type: bool
    default: false
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Get balance for a wallet
  community.lbry.lbry_wallet_balance:
    wallet_id: mywallet
  register: result
'''

RETURN = r'''
balance:
  description: Wallet balance info.
  returned: always
  type: dict
  sample: {"available": "0.0", "reserved": "0.0", "reserved_subtotals": {"claims": "0.0", "supports": "0.0", "tips": "0.0"}, "total": "0.0"}
wallet_id:
  description: The wallet id
  returned: always
  type: str
  sample: mywallet
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from ansible_collections.community.lbry.plugins.module_utils.lbry_common import (
    lbry_common_argument_spec,
    lbry_request,
    lbry_build_url,
    lbry_add_param_when_not_none,
    lbry_wallet_list,
)
import traceback


# ================
# Module execution
#

def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        wallet_id=dict(type='str', required=True, aliases=['name']),
        debug=dict(type='bool', default=False)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']
    wallet_id = module.params['wallet_id']
    debug = module.params['debug']

    r = {}
    payload = {}

    try:
        url = lbry_build_url(protocol, host, port)
        wallets = lbry_wallet_list(url)
        wallet_exists = False
        for w in wallets:
            if w['id'] == module.params['wallet_id']:
                wallet_exists = True

        if wallet_exists:
            payload["method"] = "wallet_balance"
            payload["params"] = { "wallet_id": wallet_id }
            response = lbry_request(url, payload)
            if "error" in response or "error" in response['result']:
                module.fail_json(msg='Error getting wallet info: {0}'.format(response))
            else:
                r['wallet_id'] = wallet_id
                r['balance'] = response['result']
        else:
            module.fail_json(msg="Wallet does not exist")

    except Exception as e:
        if not debug:
            module.fail_json(msg='Error running module: %s' % to_native(e))
        else:
            module.fail_json(msg='Error running module: {0}, response: {1}'.format(traceback.format_exc(), str(response)))

    module.exit_json(changed=False, **r)


if __name__ == '__main__':
    main()
