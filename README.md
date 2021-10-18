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
