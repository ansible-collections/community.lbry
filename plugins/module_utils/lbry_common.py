from __future__ import absolute_import, division, print_function
__metaclass__ = type
# from ansible.module_utils.basic import AnsibleModule, missing_required_lib
# from ansible.module_utils.six.moves import configparser
# from ansible.module_utils._text import to_native
HAS_REQUESTS = None
REQUESTS_IMP_ERR = None

import traceback
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    REQUESTS_IMP_ERR = traceback.format_exc()
import json
import socket


def lbry_common_argument_spec():
    options = dict(
        host=dict(type='str', default='127.0.0.1', aliases=['login_host']),
        port=dict(type='int', default=5279, aliases=['login_port']),
        protocol=dict(type='str', default="http"),
        debug=dict(type='bool', default=False),
    )
    return options


def lbry_build_url(protocol, host, port):
    return "{0}://{1}:{2}/".format(protocol, host, port)


def lbry_request(url, payload, headers=None):
    if headers is None:
        headers = {"Content-Type": "application/json"}  # https://tinyurl.com/2af2rd5f
    r = requests.post(url, data=json.dumps(payload), json=json.dumps(payload), headers=headers)
    return r


def lbry_valid_response(r):
    """ Does the given response look successful?
    """
    is_valid = False
    response_dict = dict(r.json())
    if r.status_code == 200 and 'result' in response_dict \
            and not isinstance(response_dict['result'], bool) \
            and 'error' not in response_dict['result']:  # for cases where result is a dict
        is_valid = True
    elif r.status_code == 200 and 'result' in response_dict \
            and isinstance(response_dict['result'], bool):  # For cases where result is a bool
        is_valid = True
    return is_valid


def lbry_error_response(r):
    """ Http request worked but there was some form of error
        on the LBRY side.
    """
    is_lbry_error = False
    response_dict = dict(r.json())
    if r.status_code == 200 and 'error' in response_dict:
        is_lbry_error = True
    elif r.status_code == 200 and 'result' in response_dict and 'error' in response_dict['result']:
        is_lbry_error = True
    return is_lbry_error


def lbry_extract_error_message(r):
    """
        Extracts the error from the lbry response
    """
    msg = None
    r = dict(r.json())
    if 'error' in r:
        if 'message' in r['error']:
            msg = r['error']['message']
    elif 'result' in r and 'error' in r['result']:
        msg = r['result']['error']
    return msg


def lbry_process_request(module, response):
    """
        @module - The Ansible module object
        @response - The response object from the lbrynet server

        This function essentially makes and process the lbry request
        and should exit the module or return the response for
        further processing
    """
    if lbry_valid_response(response):
        return dict(response.json())
    else:
        if lbry_error_response(response):
            msg = lbry_extract_error_message(response)
            module.fail_json(msg=msg)
        else:
            if module.params['debug']:
                module.fail_json(msg="Some lbry error occurred: {0}".format(response))
            else:
                module.fail_json(msg="Some lbry error occurred")


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
    response = dict(response.json())
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
    response = dict(response.json())
    return response


def lbry_account_list(url):
    payload = {
        "method": "account_list",
        "params": {"page_size": 99999}
    }
    response = lbry_request(url, payload)
    response = dict(response.json())
    return response['result']['items']


def lbry_channel_list(url):
    '''
    List all channels
    '''
    payload = {
        "method": "channel_list",
        "params": {"page_size": 99999}
    }
    response = lbry_request(url, payload)
    response = dict(response.json())
    return response['result']['items']


def lbry_address_list(url):
    payload = {
        "method": "address_list",
        "params": {"page_size": 99999}
    }
    response = lbry_request(url, payload)
    response = dict(response.json())
    return response['result']['items']
