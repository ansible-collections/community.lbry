lbry_pi
=========

This role is intended to setup a Wallet Server, for connection to the LBRY network, along with a LBRYNet instance to interact with the platform.

Please note that the Raspberry Pi 4 is significantly below the server requirements recommended so don't expect top performance. There are currently no official releases for the arm64 so we have to compile from source.

The following resources were consulted when creating this role:
* https://lbry.tech/resources/wallet-server
* https://odysee.com/@LBRYarm:5/LBRY-ARM-Guide--1---LBRYcrd:5
* https://github.com/lbryio/lbry-sdk/blob/master/INSTALL.md
* https://gitlab.melroy.org/melroy/lbry-bot/-/blob/master/lbrynet.service
* https://odysee.com/@LBRYarm:5/LBRY-ARM64-Pack1:0

Requirements
------------

* Raspberry PI 4 - 8GB Version
* Ubuntu Jammy 22.04
* 512GB SD Card (or 256GB if you're not using snapshots.)
* Python 3.7 (For lbrynet, do not use 3.8)

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

Molecule Tests
---------------

```bash
pip install molcule==3.6.* molecule-docker==1.1.* molecule-vagrant==1.0.*
```

License
-------

BSD

Author Information
------------------

Rhys Campbell - @rhysmeister
