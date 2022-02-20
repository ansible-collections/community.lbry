===============================
Community.MongoDB Release Notes
===============================

.. contents:: Topics

v0.1.0
=======

Release Summary
---------------

Initial release of the LBRY Ansible Collection.

New Modules
-----------

- community.lbry_account - Manage LBRY accounts.
- community.lbry_account_balance - Return the balance of an account.
- community.lbry_account_fund - Transfer LBC from one account to another.
- community.lbry_account_list - List details of all of the accounts.
- community.lbry_account_send - Send the same number of credits to multiple addresses from a specific account (or default account).
- community.lbry_address_is_mine - Checks if an address is associated with the current wallet.
- community.lbry_address_list - List account addresses.
- community.lbry_address_unused - Return an address containing no balance.
- community.lbry_channel - Manage LBRY channels.
- community.lbry_ffmpeg_find - Get ffmpeg installation information.
- community.lbry_get - Download stream from a LBRY name.
- community.lbry_publish - Create or replace a stream claim at a given name.
- community.lbry_resolve - Get the claim that a URL refers to.
- community.lbry_routing_table_get - Get lbry  DHT routing information.
- community.lbry_settings - Get and set lbry daemon settings.
- community.lbry_status - Get lbry daemon status.
- community.lbry_stop - Stop the lbry daemon.
- community.lbry_version - Get lbry version info.
- community.lbry_wallet - Manage LBRY Wallets.
- community.lbry_wallet_balance - Return the balance of a wallet.
- community.lbry_wallet_info - Get wallet status info.