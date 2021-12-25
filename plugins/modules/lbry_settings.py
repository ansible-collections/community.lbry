#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Rhys Campbell (@rhysmeister) <rhyscampbell@bluewin.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: lbry_settings
short_description: Get and set lbry daemon settings.
description:
  - Get and set lbry daemon settings.
author: Rhys Campbell (@rhysmeister)
version_added: "1.0.0"
extends_documentation_fragment:
  - community.lbry.lbry_common_options
options:
  parameter:
    description:
      - The LBRY Daemon Parameter to set.
    type: str
    required: true
    aliases:
      - param
  value:
    description:
      - The parameter setting.
    type: raw
    required: true
  parameter_type:
    description:
      - The type of the parameter.
    type: str
    choices:
      - str
      - int
      - float
      - bool
    default: str
    aliases:
      - type
requirements:
  - requests
'''

EXAMPLES = r'''
- name: Set peer_connect_timeout to 5.0
  community.lbry.lbry_settings:
    parameter: peer_connect_timeout
    value: 5.0
    parameter_type: float

- name: Set use_upnp to false
  community.lbry.lbry_settings:
    parameter: use_upnp
    value: false
    type: bool

- name: Set wallet_dir
  community.lbry.lbry_settings:
    parameter: wallet_dir
    value: "/tmp/tmpd_du30j6"
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
)


def cast_param_value(param_value, param_type):
    if param_type == 'str':
        param_value = str(param_value)
    elif param_type == 'bool':
        param_value = bool(param_value)
    elif param_type == 'int':
        param_value = int(param_value)
    elif param_type == 'float':
        param_value = float(param_value)
    return param_value


# ================
# Module execution
#


def main():
    argument_spec = lbry_common_argument_spec()
    argument_spec.update(
        parameter=dict(type='str', required=True, aliases=['param']),
        value=dict(type='raw', required=True),
        parameter_type=dict(type='str', default='str', choices=['str', 'int', 'bool', 'float'], aliases=['type']),
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
    parameter = module.params['parameter']
    value = module.params['value']
    parameter_type = module.params['parameter_type']
    value = cast_param_value(value, parameter_type)
    changed = None

    response = {}
    result = {}

    try:
        url = lbry_build_url(protocol, host, port)
        payload = {
            "method": "settings_get",
            "params": {}
        }
        response = lbry_request(url, payload)
        if 'result' not in response:
            module.fail_json(msg="Failed getting lbry daemon settings")
        else:
            if parameter not in response['result']:
                module.fail_json(msg="parameter not found in lbry daemon settings")
            else:
                if value == response['result'][parameter]:
                    changed = False
                    result['msg'] = "{0} is already set to {1}".format(parameter, value)
                else:
                    if module.check_mode:
                        changed = True
                        result['msg'] = "{0} was set to {1}".format(parameter, value)
                    else:
                        payload = {
                            "method": "settings_set",
                            "params": {"key": parameter,
                                       "value": value}
                        }
                        response = lbry_request(url, payload)
                        if 'result' not in response:
                            module.fail_json(msg="Failed getting lbry daemon settings")
                        if parameter not in response['result']:
                            module.fail_json(msg="parameter not found in lbry daemon settings")
                        if value != response['result'][parameter]:
                            module.fail_json(msg="parameter was not correctly set")
                        else:
                            changed = True
                            result['msg'] = "{0} was set to {1}".format(parameter, value)
    except Exception as e:
        module.fail_json(msg='Error connecting to lbry server: %s' % to_native(e))

    module.exit_json(changed=changed, **result)


if __name__ == '__main__':
    main()
