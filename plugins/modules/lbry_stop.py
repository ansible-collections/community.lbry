#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_stop
short_description: Stop the lbry daemon.
description:
  - Stop the lbry daemon.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Stop the lbry daemon
  community.lbry.lbry_stop:
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
    lbry_port_open
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

    protocol = module.params['protocol']
    host = module.params['host']
    port = module.params['port']

    response = {}

    try:

        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "stop",
            "params": {}
        }
        r = {}
        if lbry_port_open(host, port):
            if not module.check_mode:
                response = lbry_request(url, payload)
            else:
                response['result'] = "Shutting down"
            changed = True
        else:
            changed = False
            response['result'] = "lbry port already closed"
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=changed, **response)


if __name__ == '__main__':
    main()
