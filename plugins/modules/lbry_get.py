#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_get
short_description: Download stream from a LBRY name.
description:
  - Download stream from a LBRY name.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
options:
  uri:
    description:
      - uri of the content to download
    type: str
    required: yes
  file_name:
    description:
      - specified name for the downloaded file, overrides the stream file name
    type: str
  download_directory:
    description:
      - full path to the directory to download into
    type: str
  timeout:
    description:
      - download timeout in number of seconds
    type: int
  save_file:
    description:
      - save the file to the downloads directory
    type: bool
  wallet_id:
    description:
      - wallet to check for claim purchase receipts
    type: str
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Get lbry version info
  community.lbry.lbry_get:
    uri: TODO
    download_directory: /lbry/downloads
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
    lbry_process_request,
)

# ================
# Module execution
#


def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        uri=dict(type='str', required=True),
        file_name=dict(type='str'),
        download_directory=dict(type='str'),
        timeout=dict(type='int'),
        save_file=dict(type='bool'),
        wallet_id=dict(type='str'),
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
            "method": "get",
            "params": {}
        }
        request_params = {}
        for item in ['uri', 'file_name', 'download_directory', 'timeout', 'save_file', 'wallet_id']:
            payload['params'] = lbry_add_param_when_not_none(request_params, module, item)
        response = lbry_request(url, payload)
        lbry_process_request(module, response)
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=False, **response)


if __name__ == '__main__':
    main()
