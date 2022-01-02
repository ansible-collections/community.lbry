#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_account

short_description: Manage LBRY accounts.

description:
  - Manage LBRY accounts.
  - Add and remove accounts.

author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"

extends_documentation_fragment:
  - community.lbry.lbry_common_options

options:
  name:
    description:
      - The name of the account
    type: str
    required: true
  state:
    description:
      - The desired state of the account.
    type: str
    choices:
      - "present"
      - "absent"
    default: "present"
  single_key:
    description:
      - Create single key account.
    type: bool
    default: false
  wallet_id:
    description:
      - Restrict operation to specific wallet.
    type: str
  debug:
    description:
      - Show additional debug output.
    type: bool
    default: false

requirements:
  - requests
'''

EXAMPLES = r'''
- name: Create an account
  community.lbry.lbry_account:
    name: rhys
    state: present

- name: Remove an account
  community.lbry.lbry_account:
    name: rhys
    state: absent
'''

RETURN = r'''
msg:
  description: A brief description of what happened.
  returned: always
  type: str
  sample: "Account created"
account_details:
  description: Details of the account as returned by the account action.
  returned: when account_details module parameter is true
  type: dict
  sample: |
    {"address_generator": {"change": {"gap": 6, "maximum_uses_per_address": 1}, "name": "deterministic-chain",
     "receiving": {"gap": 20, "maximum_uses_per_address": 1}}, "encrypted": false, "id": "bMPwucZGFEjFqTk7EcSVyzEyCCp6Vif9yf",
     "is_default": false, "ledger": "lbc_mainnet", "modified_on": 1632675624, "name": "rhys", "private_key": "myprivatekey",
     "public_key": "mypublickey", "seed": "shadow reject anchor chief stove sick fitness address hen pave give claw"}
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from ansible_collections.community.lbry.plugins.module_utils.lbry_common import (
    lbry_common_argument_spec,
    lbry_request,
    lbry_build_url,
    lbry_add_param_when_not_none,
    lbry_account_list,
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
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        single_key=dict(type='bool', default=False),
        wallet_id=dict(type='str'),
        debug=dict(type='bool', default=False),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if not HAS_REQUESTS:
        module.fail_json(msg=missing_required_lib('requests'),
                         exception=REQUESTS_IMP_ERR)

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']
    account_name = module.params['name']
    state = module.params['state']
    debug = module.params['debug']

    response = {}

    try:
        url = lbry_build_url(protocol, host, port)
        accounts = lbry_account_list(url)
        account_exists = False
        account_id = None
        r = {}

        for a in accounts:
            if a['name'] == account_name:
                account_exists = True
                account_id = a['id']

        if state == "present":
            if not account_exists:
                if not module.check_mode:
                    url = lbry_build_url(protocol, host, port)
                    payload = {
                        "method": "account_create",
                        "params": {}
                    }
                    request_params = {}
                    for item in ['wallet_id', 'single_key']:
                        payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
                    payload['params']['account_name'] = account_name
                    response = lbry_request(url, payload)
                    response = response.json()
                    if "error" in response or "error" in response['result']:
                        module.fail_json(msg='Error creating lbry account: {0}'.format(response))
                    r['account_details'] = response['result']
                changed = True
                r['msg'] = "Account created"
            else:
                changed = False
                r['msg'] = "Account already exists"
        elif state == "absent":
            if not account_exists:
                module.exit_json(changed=False, msg="Account does not exist")
            else:
                url = lbry_build_url(protocol, host, port)
                payload = {
                    "method": "account_remove",
                    "params": {"account_id": account_id}
                }
                if not module.check_mode:
                    response = lbry_request(url, payload)
                    response = response.json()
                    if "error" in response or "error" in response['result']:
                        module.fail_json(msg='Error removing lbry account: {0}'.format(response))
                    r['account_details'] = response['result']
                changed = True
                r['msg'] = "Account removed"
    except Exception as e:
        if not debug:
            module.fail_json(msg='Error running module: %s' % to_native(e))
        else:
            module.fail_json(msg='Error running module: {0}, response: {1}, payload {2}'.format(traceback.format_exc(), str(response), str(payload)))

    module.exit_json(changed=changed, **r)


if __name__ == '__main__':
    main()
