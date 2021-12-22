# UNDER CONSTRUCTION

* This is a work in progress.
* If you want to learn about LBRY start here [LBRY](https://lbry.tech).
* Then please come back and help us out here.
* ~~As of October 2021 there are still a few show-stopping bugs to fix. This probably prevents any productive usage of the modules for the moment.~~
* CI Working as of December 21.12.2021 in a regtest environment. Some productive use of the module should be possible but expect the experience to be rocky.

# Build the Docker Image for LBRY

```
cd docker
docker build -t lbry-net:v1 .
```

# Run the LBRY Docker image

```
docker run -ti -p 5279:5279 -p 5280:5280 lbry-net:v1
```

# Run a few test commands against the server

```
curl -d'{"method": "version", "params": {}}' http://0.0.0.0:5279
curl -d'{"method": "status", "params": {}}' http://0.0.0.0:5279
curl -d'{"method": "ffmpeg_find", "params": {}}' http://0.0.0.0:5279
```

# Check settings

```
curl -d'{"method": "settings_get", "params": {}}' http://0.0.0.0:5279
```

# API Calls

## Create an Account

```
curl -d'{"method": "account_create", "params": {"account_name": "rhystest", "single_key": false}}' http://localhost:5279/
```

Returned Data - Duplicates by name can be created

```
{
  "jsonrpc": "2.0",
  "result": {
    "address_generator": {
      "change": {
        "gap": 6,
        "maximum_uses_per_address": 1
      },
      "name": "deterministic-chain",
      "receiving": {
        "gap": 20,
        "maximum_uses_per_address": 1
      }
    },
    "encrypted": false,
    "id": "bSBJKh7MJqgUJYkkTQow9sbU6iQ2nEstZd",
    "is_default": false,
    "ledger": "lbc_mainnet",
    "modified_on": 1628012162,
    "name": "rhystest",
    "private_key": "xprv9s21ZrQH143K4GuvPt7g4B4zpUmAnk6UMpUNfSmAJhzR1eVtfwwQHqycJw79QaB28i2dGs6kXf3kwNRy1QQgaAiwAqyuZndRftGKcSeznNu",
    "public_key": "xpub661MyMwAqRbcGkzPVuegRK1jNWbfCCpKj3PyTqAms3XPtSq3DVFeqeJ6ABiiwj5yrD41vAmqwUSRZ63jAWYZBFuq617PZcAR6cGAHBojTwB",
    "seed": "delay unveil joy common adapt first expect field such raven eternal curve"
  }
}
```

## Check Account Wallet Balance

curl -d'{"method": "account_balance", "params": {"account_id": "bSBJKh7MJqgUJYkkTQow9sbU6iQ2nEstZd"}}' http://localhost:5279/

Returned Data

```
{
  "jsonrpc": "2.0",
  "result": {
    "available": "0.0",
    "reserved": "0.0",
    "reserved_subtotals": {
      "claims": "0.0",
      "supports": "0.0",
      "tips": "0.0"
    },
    "total": "0.0"
  }
}
```

## Create a Channel

curl -d'{"method": "channel_create", "params": {"name": "@rhysmeister", "bid": "1.0", "featured": [], "tags": ["test"], "languages": ["en"], "account_id": "bSBJKh7MJqgUJYkkTQow9sbU6iQ2nEstZd", "preview": false, "blocking": false}}' http://localhost:5279/

Error Response

```
{
  "error": {
    "code": -32500,
    "data": {
      "args": [],
      "command": "channel_create",
      "kwargs": {
        "account_id": "bSBJKh7MJqgUJYkkTQow9sbU6iQ2nEstZd",
        "bid": "1.0",
        "blocking": false,
        "featured": [],
        "languages": [
          "en"
        ],
        "name": "@rhysmeister",
        "preview": false,
        "tags": [
          "test"
        ]
      },
      "name": "InsufficientFundsError",
      "traceback": [
        "Traceback (most recent call last):",
        "  File \"/lbry-sdk/lbry/extras/daemon/daemon.py\", line 693, in _process_rpc_call",
        "    result = await result",
        "  File \"/lbry-sdk/lbry/extras/daemon/daemon.py\", line 2612, in jsonrpc_channel_create",
        "    name, claim, amount, claim_address, funding_accounts, funding_accounts[0]",
        "  File \"/lbry-sdk/lbry/wallet/transaction.py\", line 863, in create",
        "    raise e",
        "  File \"/lbry-sdk/lbry/wallet/transaction.py\", line 825, in create",
        "    raise InsufficientFundsError()",
        "lbry.error.InsufficientFundsError: Not enough funds to cover this transaction.",
        ""
      ]
    },
    "message": "Not enough funds to cover this transaction."
  },
  "jsonrpc": "2.0"
}
```


## Debugging http

MacOS

```
brew install mitmproxy
```

# collection_template
You can build a new repository for an Ansible Collection using this template by following [Creating a repository from a template](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template). This README.md contains recommended headings for your collection README.md, with comments describing what each section should contain. Once you have created your collection repository, delete this paragraph and the title above it from your README.md.

# Foo Collection for Ansible
<!-- Add CI and code coverage badges here. Samples included below. -->
[![CI](https://github.com/ansible-collections/REPONAMEHERE/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/REPONAMEHERE/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/REPONAMEHERE)](https://codecov.io/gh/ansible-collections/REPONAMEHERE)

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Communication

<!--List available communication channels. In addition to channels specific to your collection, we also recommend to use the following ones.-->

We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). Be sure you are [subscribed](https://eepurl.com/gZmiEP).

Join us in the `#ansible` (general use questions and support), `#ansible-community` (community and collection development questions), and other [IRC channels](https://docs.ansible.com/ansible/devel/community/communication.html#irc-channels).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Contributing to this collection

<!--Describe how the community can contribute to your collection. At a minimum, fill up and include the CONTRIBUTING.md file containing how and where users can create issues to report problems or request features for this collection. List contribution requirements, including preferred workflows and necessary testing, so you can benefit from community PRs. If you are following general Ansible contributor guidelines, you can link to - [Ansible Community Guide](https://docs.ansible.com/ansible/devel/community/index.html). List the current maintainers (contributors with write or higher access to the repository). The following can be included:-->

The content of this collection is made by people like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](MAINTAINING.md).

## Governance

<!--Describe how the collection is governed. Here can be the following text:-->

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Tested with Ansible

<!-- List the versions of Ansible the collection has been tested with. Must match what is in galaxy.yml. -->

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->

### Supported connections
<!-- Optional. If your collection supports only specific connection types (such as HTTPAPI, netconf, or others), list them here. -->

## Included content

<!-- Galaxy will eventually list the module docs within the UI, but until that is ready, you may need to either describe your plugins etc here, or point to an external docsite to cover that information. -->

## Using this collection

<!--Include some quick examples that cover the most common use cases for your collection content. It can include the following examples of installation and upgrade (change NAMESPACE.COLLECTION_NAME correspondingly):-->

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install NAMESPACE.COLLECTION_NAME
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: NAMESPACE.COLLECTION_NAME
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install NAMESPACE.COLLECTION_NAME --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install NAMESPACE.COLLECTION_NAME:==0.1.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Release notes

See the [changelog](https://github.com/ansible-collections/REPONAMEHERE/tree/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
>>>>>>> c85fc108c8d3fe0e039a6e4aa73b14180a58590e
