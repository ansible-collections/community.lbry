#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_version
short_description: Get lbry version info.
description:
  - Get lbry version info.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Get lbry version info
  community.lbry.lbry_version:
  register: result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from ansible_collections.community.lbry.plugins.module_utils.lbry_common import (
    lbry_common_argument_spec,
    lbry_request,
    lbry_build_url,
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

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']

    try:
        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "version",
            "params": {}
        }
        response = lbry_request(url, payload)
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=False, **response)


if __name__ == '__main__':
    main()
