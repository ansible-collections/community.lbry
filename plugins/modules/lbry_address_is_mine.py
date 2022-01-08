#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_address_is_mine
short_description: Checks if an address is associated with the current wallet.
description:
  - Checks if an address is associated with the current wallet.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options

options:
  address:
    description:
      - address to check.
    type: str
    required: yes
  account_id:
    description:
      - id of the account to use.
    type: str
  wallet_id:
    description:
      - restrict operation to specific wallet.
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
- name: Check if an address belowngs to the default account/wallet
  community.lbry.lbry_address_is_mine:
    address: "mxCb2mjmyDRXYdPGkC6QRqjMwpTL2wVoVe"
  register: result
'''

RETURN = r'''
is_mine:
  description: Is the address yours?
  type: bool
  returned: on success
  sample: true
msg:
  description. what went wrong.
  type: str
  returned: on error
  sample: "The module returned an invalid result of type str"
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from ansible_collections.community.lbry.plugins.module_utils.lbry_common import (
    lbry_common_argument_spec,
    lbry_request,
    lbry_build_url,
    lbry_add_param_when_not_none,
    lbry_process_request,
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
        address=dict(type='str', required=True),
        account_id=dict(type='str'),
        wallet_id=dict(type='str'),
        debug=dict(type='bool', default=False),
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
    r = {}

    try:
        url = lbry_build_url(protocol, host, port)
        payload = {
          "method": "address_is_mine",
          "params": {}
        }
        request_params = {}
        for item in module.params:
          if item not in ['host', 'port', 'protocol', 'debug']:
              payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
        response = lbry_request(url, payload)
        if 'result' in response and isinstance(response['result'], bool):  # good result
            is_mine = response['result']
        else:
            module.fail_json(msg="The module returned an unexpected result: {0}".format(response))
    except Exception as e:
        if not debug:
            module.fail_json(msg='Error running module: %s' % to_native(e))
        else:
            module.fail_json(msg='Error running module: {0}'.format(traceback.format_exc()))

    module.exit_json(changed=False, is_mine=is_mine)


if __name__ == '__main__':
    main()
