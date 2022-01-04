#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_account_list
short_description: List details of all of the accounts.
description:
  - List details of all of the accounts.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options

options:
  debug:
    description:
      - Show additional debug output.
    type: bool
    default: false
requirements:
  - requests
'''

EXAMPLES = r'''
- name: List all the accounts
  community.lbry.lbry_account_list:
  register: result
'''

RETURN = r'''
accounts:
  description: List of dicts providing the accounts available.
  type: list
  returned: on success
  sample: [
        {
            "id": "account_id",
            "is_default": "this account is used by default",
            "ledger": "name of crypto currency and network",
            "name": "optional account name",
            "seed": "human friendly words from which account can be recreated",
            "encrypted": "if account is encrypted",
            "private_key": "extended private key",
            "public_key": "extended public key",
            "address_generator": "settings for generating addresses",
            "modified_on": "date of last modification to account settings"
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from ansible_collections.community.lbry.plugins.module_utils.lbry_common import (
    lbry_common_argument_spec,
    # lbry_request,
    lbry_build_url,
    # lbry_add_param_when_not_none,
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
        debug=dict(type='bool', default=False)
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
    debug = module.params['debug']
    r = {}

    try:
        url = lbry_build_url(protocol, host, port)
        accounts = lbry_account_list(url)
        if len(accounts) == 0:
            module.fail_json(msg="Error getting accounts list. Server responded with a zero-length list.")
        else:
            r['accounts'] = accounts
    except Exception as e:
        if not debug:
            module.fail_json(msg='Error running module: %s' % to_native(e))
        else:
            module.fail_json(msg='Error running module: {0}'.format(traceback.format_exc()))

    module.exit_json(changed=False, **r)


if __name__ == '__main__':
    main()
