from __future__ import absolute_import, division, print_function
__metaclass__ = type
#from ansible.module_utils.basic import AnsibleModule, missing_required_lib
#from ansible.module_utils.six.moves import configparser
#from ansible.module_utils._text import to_native

import requests
import json
import socket


def lbry_common_argument_spec():
    options = dict(
        host=dict(type='str', default='127.0.0.1'),
        port=dict(type='int', default=5279),
        protocol=dict(type='str', default="http"),
        debug=dict(type='bool', default=False),
    )
    return options


def lbry_build_url(protocol, host, port):
    return f"{protocol}://{host}:{port}/".format(protocol, host, port)


def lbry_request(url, payload, headers={"Content-Type": "application/json"}):
    r = requests.post(url, data=json.dumps(payload), json=json.dumps(payload), headers=headers)
    if r.status_code == 200 and 'result' in r.json():
        return dict(r.json())
    else:
        raise Exception("Invalid response received. status code: {0}, Response: {1}".format(r.status_code, r.text))


def lbry_port_open(host, port):
    open = False
    lbry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, port)
    result_of_check = lbry_socket.connect_ex(location)
    if result_of_check == 0:
        open = True
    lbry_socket.close()
    return open


def lbry_add_param_when_not_none(request_params, module, param_name):
    '''
    @payload - dict object that we post to lbry
    @module - Ansible Module object
    @param_name - The name of the param
    '''
    if module.params[param_name] is not None:
        request_params[param_name] = module.params[param_name]
    return request_params


def lbry_wallet_list(url):
    '''
    List all loaded wallets
    '''
    payload = {
        "method": "wallet_list",
        "params": {}
        }
    response = lbry_request(url, payload)
    return response['result']['items']


def lbry_wallet_status(url):
    '''
    Return a dictionary in the following format assuming the wallet exists
    {
        'jsonrpc': '2.0',
        'result':
        {
            'is_encrypted': False,
            'is_locked': False,
            'is_syncing': False
        }
    }
    '''
    payload = {
        "method": "wallet_status",
        "params": {}
    }
    response = lbry_request(url, payload)
    return response


def lbry_account_list(url):
    payload = {
        "method": "account_list",
        "params": { "page_size": 99999 }
        }
    response = lbry_request(url, payload)
    return response['result']['items']
