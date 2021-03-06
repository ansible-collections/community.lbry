#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_ffmpeg_find
short_description: Get ffmpeg installation information.
description:
  - Get ffmpeg installation information.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Get ffmpeg installation information.
  community.lbry.lbry_ffmpeg_find:
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
    HAS_REQUESTS,
    REQUESTS_IMP_ERR,
    lbry_process_request,
)


# ================
# Module execution
#

def main():
    argument_spec = lbry_common_argument_spec()
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

    response = {}

    try:

        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "ffmpeg_find",
            "params": {}
        }
        response = lbry_request(url, payload)
        response = lbry_process_request(module, response)
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=False, **response)


if __name__ == '__main__':
    main()
