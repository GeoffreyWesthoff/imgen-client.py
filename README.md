# imgen-client.py

A python wrapper for Dank Memer's Image Generation API (Imgen)

## Installation

This version of imgen-client.py is currently not in a consumer ready state. 

There is currently no documentation on the installation or usage process.

#### YOU ARE ON YOUR OWN FOR NOW

## Requirements
* aiohttp
* requests

Python 3.4 is a bare minimum and we do not test in older Python versions.
We strongly recommend using the latest stable version.
At the time of writing, this version is 3.7.4

#### ANY VERSION BELOW PYTHON 3.4, INCLUDING PYTHON 2 IS NOT SUPPORTED!

## Example
Awaitables must be inside an async function, but this is omitted for clarity.
SyncClient supports the same functions, but uses requests instead of aiohttp.
SyncClient does not support ratelimit buckets however.

### Async 
```python
from imgen import AsyncClient
async_client = AsyncClient(token='tokengoeshere')

# Create image
await async_client.magik.get(avatar1='urltoimage')
# Returns BytesIO, which works similiarly to f = open('file')

# Create image and save to disk
await async_client.magik.save(filename='magiked', avatar1='urltoimage')
# Saves image with filename to disk. Returns None

# Create image and pass directly to a discord File. Useful for bot creators
f = await async_client.magik.get_as_discord(avatar1='urltoimage')
# Returns discord.File. Send using await Messageable.send(file=f)


# List all available endpoints
print(async_client.endpoints)
# Returns tuple
```

### Sync
```python
# Sync
from imgen import SyncClient
sync_client = SyncClient(token='tokengoeshere')

# Create image
sync_client.magik.get(avatar1='urltoimage')
# Returns BytesIO, which works similiarly to f = open('file')

# Create image and save to disk
sync_client.magik.save(filename='magiked', avatar1='urltoimage')
# Saves image with filename to disk. Returns None

# Create image and pass directly to a discord File. Useful for bot creators
f = sync_client.magik.get_as_discord(avatar1='urltoimage')
# Returns discord.File. Send using await Messageable.send(file=f)
```

## Documentation
Coming Soon

## Special Thanks

Rapptz for writing a ratelimit bucket system that has greatly inspired the system used here!
