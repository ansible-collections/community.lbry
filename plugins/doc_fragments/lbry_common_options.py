from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = r'''
options:
  host:
    description:
      - The LBRY SDK Server Hostname.
    type: str
    default: 127.0.0.1
    aliases:
      - "login_host"
  port:
    description:
      - The LBRY SDK Server Port.
    type: int
    default: 5279
    aliases:
      - "login_port"
  protocol:
    description:
      - The LBRY SDK Server Protocol.
    type: str
    default "http"
  debug:
    description:
      - Enable additional debug output.
    type: bool
    default: False
'''
