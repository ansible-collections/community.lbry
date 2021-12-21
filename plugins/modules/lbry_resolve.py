#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_resolve
short_description: Get the claim that a URL refers to.
description:
  - Get the claim that a URL refers to.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
options:
  urls:
    description:
      - uri of the content to download
    type: list
    elements: str
    required: yes
  wallet_id:
    description:
      - wallet to check for claim purchase receipts
    type: str
  new_sdk_server:
    description:
      - URL of the new SDK server (EXPERIMENTAL).
    type: str
  include_purchase_receipt:
    description:
      - lookup and include a receipt if this wallet has purchased the claim being resolved.
    type: bool
    default: false
  include_is_my_output:
    description:
      - lookup and include a boolean indicating if claim being resolved is yours.
    type: bool
    default: false
  include_sent_supports:
    description:
      - lookup and sum the total amount of supports you've made to this claim.
    type: bool
    default: false
  include_sent_tips:
    description:
      - lookup and sum the total amount of tips you've made to this claim (only makes sense when claim is not yours)
    type: bool
    default: false
  include_received_tips:
    description:
      - lookup and sum the total amount of tips you've received to this claim (only makes sense when claim is yours)
    type: bool
    default: false
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Get a claim
  community.lbry.lbry_resolve:
    uri: TODO
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
)

# ================
# Module execution
#


def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        urls=dict(type='list', elements='str', required=True),
        wallet_id=dict(type='str'),
        new_sdk_server=dict(type='str', default=None),
        include_purchase_receipt=dict(type='bool', default=False),
        include_is_my_output=dict(type='bool', default=False),
        include_sent_supports=dict(type='bool', default=False),
        include_sent_tips=dict(type='bool', default=False),
        include_received_tips=dict(type='bool', default=False),
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

    try:
        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "resolve",
            "params": {}
        }
        request_params = {}
        for item in ['urls', 'wallet_id', 'new_sdk_server', 'include_purchase_receipt',
                     'include_is_my_output', 'include_sent_supports', 'include_sent_tips',
                     'include_received_tips']:
            payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
        response = lbry_request(url, payload)
        error_count = 0
        for url in module.params['urls']:  # we fail when all files fail to resolve
            if "error" in response['result'][url]:
                error_count += 1
            if error_count == len(module.params['urls']):
                module.fail_json(msg='Error resolving file(s) from lbrynet: {0}'.format(response))
    except Exception as e:
        module.fail_json(msg='Error resolving file from lbrynet: %s' % to_native(e))

    module.exit_json(changed=False, **response)


if __name__ == '__main__':
    main()
