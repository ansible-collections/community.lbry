#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_wallet_create
short_description: Create a new wallet.
description:
  - Create a new wallet.
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
  skip_on_startup:
    description:
      - don't add wallet to daemon_settings.yml
    type: bool
  create_account:
    description:
      - generates the default account
    type: bool
  single_key:
    description:
      - used with create_account, creates single-key account
    type: bool
  state:
    description:
      - State of the wallet
    type: str
    choices:
      - present
      - absent
      - locked
      - unlocked
      - encrypted
      - decrypted
      - loaded
      - unloaded
  password:
    description:
      - Password for encryping or decrypting wallets.
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
- name: Create a new wallet
  community.lbry.lbry_wallet:
    wallet_id: mywallet
    state: present
  register: result
'''

RETURN = r'''
msg:
  description: A brief description of what happened.
  returned: always
  type: str
  sample: "Wallet created"
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
    lbry_wallet_status
)
import traceback


# ================
# Module execution
#

def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        wallet_id=dict(type='str', required=True, aliases=['name']),
        skip_on_startup=dict(type='bool'),
        create_account=dict(type='bool'),
        single_key=dict(type='bool'),
        state=dict(type='str', choices=['present', 'absent', 'locked', 'unlocked', 'encrypted', 'decrypted', 'loaded', 'unloaded'], default='present'),
        password=dict(type='str', default=None, no_log=True),
        debug=dict(type='bool', default=False)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']
    state = module.params['state']
    wallet_id = module.params['wallet_id']
    new_password = module.params['password']
    debug = module.params['debug']
    if state in ['encrypted', 'decrypted'] and new_password is None:
        module.fail_json(msg='You must supply a password when encrypting or decrypting a wallet')
    changed = False
    response = None

    r = {}

    try:
        url = lbry_build_url(protocol, host, port)
        wallets = lbry_wallet_list(url)
        wallet_exists = False
        for w in wallets:
            if w['id'] == module.params['wallet_id']:
                wallet_exists = True

        payload = {}
        request_params = {}
        for item in module.params:
            if item not in ['host', 'port', 'protocol', 'debug', 'state']:
                payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
        if state == 'present':
            if not wallet_exists:
                if not module.check_mode:
                    payload['method'] = "wallet_create"
                    payload['params'] = request_params
                    response = lbry_request(url, payload)
                    if debug:
                        r['response'] = str(response)
                    if "error" in response or "error" in response['result']:
                        module.fail_json(msg=f'Error creating wallet: {response}')
                changed = True
                r['msg'] = "Wallet created"
            else:
                r['msg'] = "Wallet already exists"
        elif state == 'absent':
            if not wallet_exists:
                module.exit_json(changed=False, msg="Wallet does not exist")
            else:
                payload['method'] = "wallet_remove"
                payload["params"] = { "wallet_id": wallet_id }
                if not module.check_mode:
                    response = lbry_request(url, payload)
                    if debug:
                        r['response'] = str(response)
                    if "error" in response or "error" in response['result']:
                        module.fail_json(msg=f'Error removing wallet: {response}')
                changed = True
                r['msg'] = 'Wallet removed'
        elif state == 'locked':  # TODO cannot locked an unencrypted wallet check this
            if not wallet_exists:
                module.fail_json(msg="You cannot lock a wallet that does not exist")
            else:
                wallet_status = lbry_wallet_status(url)
                if wallet_status['result']['is_locked']:
                    module.exit_json(changed=False, msg="Wallet is already locked")
                else:
                    if wallet_status['result']['is_encrypted']:
                        payload['method'] = "wallet_lock"
                        payload["params"] = { "wallet_id": wallet_id }
                        if not module.check_mode:
                            response = lbry_request(url, payload)
                            if debug:
                                r['response'] = str(response)
                            if "error" in response or "error" in response['result']:
                                module.fail_json(msg=f'Error locking wallet: {response}')
                        changed = True
                        r['msg'] = 'Wallet locked'
                    else:
                        changed = False
                        module.fail_json(msg='Wallet must be encrypted before locking', wallet_status=str(wallet_status))
        elif state == 'unlocked':
            if not wallet_exists:
                module.fail_json(msg="You cannot unlock a wallet that does not exist")
            else:
                wallet_status = lbry_wallet_status(url)
                if not wallet_status['result']['is_locked']:
                    module.exit_json(changed=False, msg="Wallet is already unlocked")
                else:
                    payload['method'] = "wallet_unlock"
                    payload["params"] = { "wallet_id": wallet_id }
                    if not module.check_mode:
                        response = lbry_request(url, payload)
                        if debug:
                            r['response'] = str(response)
                        if "error" in response or "error" in response['result']:
                            module.fail_json(msg=f'Error unlocking wallet: {response}')
                    changed = True
                    r['msg'] = 'Wallet unlocked'
        elif state == 'encrypted':
            if not wallet_exists:
                module.fail_json(msg="You cannot encrypt a wallet that does not exist")
            else:
                wallet_status = lbry_wallet_status(url)
                if wallet_status['result']['is_encrypted']:
                    module.exit_json(changed=False, msg="Wallet is already encrypted")
                else:
                    payload["method"] = "wallet_encrypt"
                    payload["params"] = {"wallet_id":wallet_id,"new_password":new_password}
                    if not module.check_mode:
                        response = lbry_request(url, payload)
                        if debug:
                            r['response'] = str(response)
                        if "error" in response or (isinstance(response['result'], dict) and "error" in response['result']):
                            module.fail_json(msg=f'Error encrypting wallet: {response}')
                    changed = True
                    r['msg'] = 'Wallet encrypted'
                    r['payload'] = str(payload)
                    r['new_wallet_status'] = lbry_wallet_status(url)
        elif state == 'decrypted':  # TODO Check that wallet is unlocked before decrypting
            if not wallet_exists:
                module.fail_json(msg="You cannot decrypt a wallet that does not exist")
            else:
                wallet_status = lbry_wallet_status(url)
                if not wallet_status['result']['is_encrypted']:
                    module.exit_json(changed=False, msg="Wallet is already decrypted")
                else:
                    if not wallet_status['result']['is_locked']:
                        payload['method'] = "wallet_decrypt"
                        payload["params"] = { "wallet_id": wallet_id, "new_password": new_password }
                        if not module.check_mode:
                            response = lbry_request(url, payload)
                            if debug:
                                r['response'] = str(response)
                            if "error" in response or (isinstance(response['result'], dict) and "error" in response['result']):
                                module.fail_json(msg=f'Error decrypting wallet: {response}')
                        changed = True
                        r['msg'] = 'Wallet decrypted'
                    else:
                        changed = False
                        r['msg'] = 'Wallet must be unlocked before decrypting'
        elif state == 'loaded':
            if not wallet_exists:
                module.fail_json(msg="You cannot load a wallet that does not exist")
            else:
                pass  # Need a way to check a wallet exists without loading/unloading it
        elif state == 'unloaded':
            if not wallet_exists:
                module.fail_json(msg="You cannot unload a wallet that does not exist")
            else:
                 pass  # Need a way to check a wallet exists without loading/unloading it
    except Exception as e:
        if not debug:
            module.fail_json(msg='Error running module: %s' % to_native(e))
        else:
            module.fail_json(msg='Error running module: {0}, response: {1}, payload {2}'.format(traceback.format_exc(), str(response), str(payload)))


    module.exit_json(changed=changed, **r)


if __name__ == '__main__':
    main()
